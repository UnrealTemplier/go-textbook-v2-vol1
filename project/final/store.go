package bookmarkflow

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/url"
	"os"
	"path/filepath"
	"slices"
	"strings"
	"sync"
	"time"
)

var (
	// ErrNotFound возвращается при обращении к несуществующей закладке.
	ErrNotFound = errors.New("закладка не найдена")
	// ErrValidation возвращается при нарушении правил валидации входных данных.
	ErrValidation = errors.New("ошибка валидации")
)

// Bookmark — основная сущность HTTP-сервиса BookmarkFlow.
type Bookmark struct {
	ID        int       `json:"id"`
	Title     string    `json:"title"`
	URL       string    `json:"url"`
	Tags      []string  `json:"tags,omitempty"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// CreateInput описывает тело запроса на создание закладки.
type CreateInput struct {
	Title string   `json:"title"`
	URL   string   `json:"url"`
	Tags  []string `json:"tags"`
}

// UpdateInput описывает тело запроса на обновление закладки.
type UpdateInput struct {
	Title string   `json:"title"`
	URL   string   `json:"url"`
	Tags  []string `json:"tags"`
}

// ListFilter задаёт фильтрацию закладок по тегу и текстовому запросу.
type ListFilter struct {
	Tag   string
	Query string
}

// Store описывает контракт хранилища закладок.
// В Томе 2 эту же границу легко переключить с JSON-файла на базу данных без правок HTTP-слоя.
type Store interface {
	Create(in CreateInput) (Bookmark, error)
	Get(id int) (Bookmark, error)
	List(filter ListFilter) ([]Bookmark, error)
	Update(id int, in UpdateInput) (Bookmark, error)
	Delete(id int) error
}

// ValidateInput нормализует и проверяет название, URL и теги.
func ValidateInput(title, rawURL string, tags []string) (string, string, []string, error) {
	cleanTitle := strings.TrimSpace(title)
	if cleanTitle == "" {
		return "", "", nil, fmt.Errorf("%w: поле title обязательно", ErrValidation)
	}
	if len([]rune(cleanTitle)) > 200 {
		return "", "", nil, fmt.Errorf("%w: поле title не должно превышать 200 символов", ErrValidation)
	}

	cleanURL := strings.TrimSpace(rawURL)
	parsed, err := url.Parse(cleanURL)
	if err != nil || (parsed.Scheme != "http" && parsed.Scheme != "https") || parsed.Host == "" {
		return "", "", nil, fmt.Errorf("%w: укажите корректный http(s) URL", ErrValidation)
	}

	cleanTags := normalizeTags(tags)
	return cleanTitle, cleanURL, cleanTags, nil
}

func normalizeTags(tags []string) []string {
	var out []string
	for _, raw := range tags {
		tag := strings.ToLower(strings.TrimSpace(raw))
		if tag != "" && !slices.Contains(out, tag) {
			out = append(out, tag)
		}
	}
	slices.Sort(out)
	return out
}

// FileStore реализует Store поверх JSON-файла с потокобезопасностью (sync.RWMutex)
// и атомарной перезаписью через временный файл и os.Rename.
type FileStore struct {
	mu     sync.RWMutex
	path   string
	nextID int
	items  []Bookmark
}

type diskState struct {
	NextID int        `json:"next_id"`
	Items  []Bookmark `json:"items"`
}

// OpenFileStore открывает существующий JSON-файл или подготавливает пустое хранилище.
func OpenFileStore(path string) (*FileStore, error) {
	fs := &FileStore{
		path:   path,
		nextID: 1,
	}
	if err := fs.load(); err != nil {
		return nil, err
	}
	return fs, nil
}

func (f *FileStore) Create(in CreateInput) (Bookmark, error) {
	title, rawURL, tags, err := ValidateInput(in.Title, in.URL, in.Tags)
	if err != nil {
		return Bookmark{}, err
	}

	f.mu.Lock()
	defer f.mu.Unlock()

	now := time.Now().UTC().Truncate(time.Second)
	bm := Bookmark{
		ID:        f.nextID,
		Title:     title,
		URL:       rawURL,
		Tags:      tags,
		CreatedAt: now,
		UpdatedAt: now,
	}
	f.nextID++
	f.items = append(f.items, bm)
	if err := f.saveLocked(); err != nil {
		// Откатываем изменение в памяти, если запись на диск не удалась.
		f.items = f.items[:len(f.items)-1]
		f.nextID--
		return Bookmark{}, err
	}
	return cloneBookmark(bm), nil
}

func (f *FileStore) Get(id int) (Bookmark, error) {
	f.mu.RLock()
	defer f.mu.RUnlock()

	for _, it := range f.items {
		if it.ID == id {
			return cloneBookmark(it), nil
		}
	}
	return Bookmark{}, fmt.Errorf("%w: #%d", ErrNotFound, id)
}

func (f *FileStore) List(filter ListFilter) ([]Bookmark, error) {
	f.mu.RLock()
	defer f.mu.RUnlock()

	tag := strings.ToLower(strings.TrimSpace(filter.Tag))
	query := strings.ToLower(strings.TrimSpace(filter.Query))

	out := make([]Bookmark, 0, len(f.items))
	for _, it := range f.items {
		if tag != "" && !slices.Contains(it.Tags, tag) {
			continue
		}
		if query != "" &&
			!strings.Contains(strings.ToLower(it.Title), query) &&
			!strings.Contains(strings.ToLower(it.URL), query) {
			continue
		}
		out = append(out, cloneBookmark(it))
	}
	return out, nil
}

func (f *FileStore) Update(id int, in UpdateInput) (Bookmark, error) {
	title, rawURL, tags, err := ValidateInput(in.Title, in.URL, in.Tags)
	if err != nil {
		return Bookmark{}, err
	}

	f.mu.Lock()
	defer f.mu.Unlock()

	idx := slices.IndexFunc(f.items, func(b Bookmark) bool { return b.ID == id })
	if idx == -1 {
		return Bookmark{}, fmt.Errorf("%w: #%d", ErrNotFound, id)
	}

	prev := f.items[idx]
	updated := Bookmark{
		ID:        prev.ID,
		Title:     title,
		URL:       rawURL,
		Tags:      tags,
		CreatedAt: prev.CreatedAt,
		UpdatedAt: time.Now().UTC().Truncate(time.Second),
	}
	f.items[idx] = updated
	if err := f.saveLocked(); err != nil {
		f.items[idx] = prev
		return Bookmark{}, err
	}
	return cloneBookmark(updated), nil
}

func (f *FileStore) Delete(id int) error {
	f.mu.Lock()
	defer f.mu.Unlock()

	idx := slices.IndexFunc(f.items, func(b Bookmark) bool { return b.ID == id })
	if idx == -1 {
		return fmt.Errorf("%w: #%d", ErrNotFound, id)
	}

	prev := slices.Clone(f.items)
	f.items = slices.Delete(f.items, idx, idx+1)
	if err := f.saveLocked(); err != nil {
		f.items = prev
		return err
	}
	return nil
}

func (f *FileStore) load() error {
	data, err := os.ReadFile(f.path)
	if errors.Is(err, os.ErrNotExist) {
		return nil
	}
	if err != nil {
		return fmt.Errorf("чтение хранилища %s: %w", f.path, err)
	}
	if len(strings.TrimSpace(string(data))) == 0 {
		return nil
	}
	var state diskState
	if err := json.Unmarshal(data, &state); err != nil {
		return fmt.Errorf("разбор JSON %s: %w", f.path, err)
	}
	f.nextID = max(state.NextID, 1)
	f.items = state.Items
	return nil
}

func (f *FileStore) saveLocked() error {
	dir := filepath.Dir(f.path)
	if err := os.MkdirAll(dir, 0o755); err != nil {
		return fmt.Errorf("создание каталога %s: %w", dir, err)
	}
	data, err := json.MarshalIndent(diskState{NextID: f.nextID, Items: f.items}, "", "  ")
	if err != nil {
		return fmt.Errorf("сериализация JSON: %w", err)
	}
	return writeFileAtomic(f.path, data)
}

func writeFileAtomic(path string, data []byte) error {
	dir := filepath.Dir(path)
	tmp, err := os.CreateTemp(dir, ".bookmarkflow-*.tmp")
	if err != nil {
		return err
	}
	tmpName := tmp.Name()
	cleanup := true
	defer func() {
		if cleanup {
			_ = os.Remove(tmpName)
		}
	}()

	if _, err := tmp.Write(data); err != nil {
		_ = tmp.Close()
		return err
	}
	if err := tmp.Sync(); err != nil {
		_ = tmp.Close()
		return err
	}
	if err := tmp.Close(); err != nil {
		return err
	}
	if err := os.Rename(tmpName, path); err != nil {
		return err
	}
	cleanup = false
	return nil
}

func cloneBookmark(b Bookmark) Bookmark {
	b.Tags = slices.Clone(b.Tags)
	return b
}
