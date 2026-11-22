package step04

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"slices"
	"strings"
	"time"
)

var (
	ErrEmptyTitle = errors.New("название закладки не может быть пустым")
	ErrInvalidURL = errors.New("ссылка должна начинаться с http:// или https://")
	ErrNotFound   = errors.New("закладка не найдена")
)

// Bookmark — доменная модель закладки.
type Bookmark struct {
	ID        int       `json:"id"`
	Title     string    `json:"title"`
	URL       string    `json:"url"`
	Tags      []string  `json:"tags,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

// Validate нормализует и проверяет поля закладки.
func (b *Bookmark) Validate() error {
	b.Title = strings.TrimSpace(b.Title)
	b.URL = strings.TrimSpace(b.URL)
	if b.Title == "" {
		return ErrEmptyTitle
	}
	if !strings.HasPrefix(b.URL, "http://") && !strings.HasPrefix(b.URL, "https://") {
		return fmt.Errorf("%w: %q", ErrInvalidURL, b.URL)
	}
	b.Tags = normalizeTags(b.Tags)
	return nil
}

// Store описывает контракт хранилища закладок.
type Store interface {
	Create(b Bookmark) (Bookmark, error)
	Get(id int) (Bookmark, error)
	List() ([]Bookmark, error)
	Update(b Bookmark) (Bookmark, error)
	Delete(id int) error
	Search(query string) ([]Bookmark, error)
}

// MemoryStore хранит закладки в оперативной памяти.
type MemoryStore struct {
	nextID int
	items  []Bookmark
}

// NewMemoryStore создаёт пустое in-memory хранилище.
func NewMemoryStore() *MemoryStore {
	return &MemoryStore{nextID: 1}
}

func (m *MemoryStore) Create(b Bookmark) (Bookmark, error) {
	if err := b.Validate(); err != nil {
		return Bookmark{}, err
	}
	b.ID = m.nextID
	m.nextID++
	if b.CreatedAt.IsZero() {
		b.CreatedAt = time.Now().UTC().Truncate(time.Second)
	}
	b.Tags = slices.Clone(b.Tags)
	m.items = append(m.items, b)
	return cloneBookmark(b), nil
}

func (m *MemoryStore) Get(id int) (Bookmark, error) {
	for _, it := range m.items {
		if it.ID == id {
			return cloneBookmark(it), nil
		}
	}
	return Bookmark{}, fmt.Errorf("%w: #%d", ErrNotFound, id)
}

func (m *MemoryStore) List() ([]Bookmark, error) {
	out := make([]Bookmark, len(m.items))
	for i, it := range m.items {
		out[i] = cloneBookmark(it)
	}
	return out, nil
}

func (m *MemoryStore) Update(b Bookmark) (Bookmark, error) {
	if err := b.Validate(); err != nil {
		return Bookmark{}, err
	}
	for i, it := range m.items {
		if it.ID == b.ID {
			b.CreatedAt = it.CreatedAt
			m.items[i] = cloneBookmark(b)
			return cloneBookmark(b), nil
		}
	}
	return Bookmark{}, fmt.Errorf("%w: #%d", ErrNotFound, b.ID)
}

func (m *MemoryStore) Delete(id int) error {
	idx := slices.IndexFunc(m.items, func(b Bookmark) bool { return b.ID == id })
	if idx == -1 {
		return fmt.Errorf("%w: #%d", ErrNotFound, id)
	}
	m.items = slices.Delete(m.items, idx, idx+1)
	return nil
}

func (m *MemoryStore) Search(query string) ([]Bookmark, error) {
	q := strings.ToLower(strings.TrimSpace(query))
	if q == "" {
		return m.List()
	}
	var out []Bookmark
	for _, it := range m.items {
		if strings.Contains(strings.ToLower(it.Title), q) ||
			strings.Contains(strings.ToLower(it.URL), q) ||
			slices.Contains(it.Tags, q) {
			out = append(out, cloneBookmark(it))
		}
	}
	return out, nil
}

// FileStore сохраняет закладки в JSON-файл, переиспользуя логику MemoryStore через композицию.
type FileStore struct {
	path string
	mem  *MemoryStore
}

type fileSnapshot struct {
	NextID int        `json:"next_id"`
	Items  []Bookmark `json:"items"`
}

// OpenFileStore открывает или создаёт файловое хранилище.
func OpenFileStore(path string) (*FileStore, error) {
	fs := &FileStore{
		path: path,
		mem:  NewMemoryStore(),
	}
	if err := fs.load(); err != nil {
		return nil, err
	}
	return fs, nil
}

func (f *FileStore) Create(b Bookmark) (Bookmark, error) {
	created, err := f.mem.Create(b)
	if err != nil {
		return Bookmark{}, err
	}
	if err := f.save(); err != nil {
		return Bookmark{}, err
	}
	return created, nil
}

func (f *FileStore) Get(id int) (Bookmark, error)        { return f.mem.Get(id) }
func (f *FileStore) List() ([]Bookmark, error)           { return f.mem.List() }
func (f *FileStore) Search(q string) ([]Bookmark, error) { return f.mem.Search(q) }

func (f *FileStore) Update(b Bookmark) (Bookmark, error) {
	updated, err := f.mem.Update(b)
	if err != nil {
		return Bookmark{}, err
	}
	if err := f.save(); err != nil {
		return Bookmark{}, err
	}
	return updated, nil
}

func (f *FileStore) Delete(id int) error {
	if err := f.mem.Delete(id); err != nil {
		return err
	}
	return f.save()
}

func (f *FileStore) load() error {
	data, err := os.ReadFile(f.path)
	if errors.Is(err, os.ErrNotExist) {
		return nil
	}
	if err != nil {
		return fmt.Errorf("чтение %s: %w", f.path, err)
	}
	if len(strings.TrimSpace(string(data))) == 0 {
		return nil
	}
	var snap fileSnapshot
	if err := json.Unmarshal(data, &snap); err != nil {
		return fmt.Errorf("разбор %s: %w", f.path, err)
	}
	f.mem.nextID = max(snap.NextID, 1)
	f.mem.items = snap.Items
	return nil
}

func (f *FileStore) save() error {
	snap := fileSnapshot{NextID: f.mem.nextID, Items: f.mem.items}
	data, err := json.MarshalIndent(snap, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(f.path, data, 0o600)
}

func cloneBookmark(b Bookmark) Bookmark {
	b.Tags = slices.Clone(b.Tags)
	return b
}

func normalizeTags(tags []string) []string {
	var clean []string
	for _, raw := range tags {
		tag := strings.ToLower(strings.TrimSpace(raw))
		if tag != "" && !slices.Contains(clean, tag) {
			clean = append(clean, tag)
		}
	}
	slices.Sort(clean)
	return clean
}
