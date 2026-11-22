package step03

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

// Bookmark описывает одну сохранённую закладку.
type Bookmark struct {
	ID        int       `json:"id"`
	Title     string    `json:"title"`
	URL       string    `json:"url"`
	Tags      []string  `json:"tags,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

// FileCatalog хранит закладки и умеет сохранять их в JSON-файл.
type FileCatalog struct {
	path      string
	nextID    int
	bookmarks []Bookmark
}

type diskPayload struct {
	NextID    int        `json:"next_id"`
	Bookmarks []Bookmark `json:"bookmarks"`
}

// OpenFileCatalog загружает закладки из JSON-файла (или начинает пустой каталог, если файла нет).
func OpenFileCatalog(path string) (*FileCatalog, error) {
	c := &FileCatalog{path: path, nextID: 1}
	if err := c.Load(); err != nil {
		return nil, err
	}
	return c, nil
}

// Load считывает JSON-файл с диска.
func (c *FileCatalog) Load() error {
	data, err := os.ReadFile(c.path)
	if errors.Is(err, os.ErrNotExist) {
		c.nextID = 1
		c.bookmarks = nil
		return nil
	}
	if err != nil {
		return fmt.Errorf("чтение файла закладок: %w", err)
	}
	if len(strings.TrimSpace(string(data))) == 0 {
		c.nextID = 1
		c.bookmarks = nil
		return nil
	}

	var payload diskPayload
	if err := json.Unmarshal(data, &payload); err != nil {
		return fmt.Errorf("разбор JSON закладок: %w", err)
	}
	c.nextID = max(payload.NextID, 1)
	c.bookmarks = payload.Bookmarks
	return nil
}

// Save записывает текущее состояние каталога на диск в формате JSON.
func (c *FileCatalog) Save() error {
	payload := diskPayload{
		NextID:    c.nextID,
		Bookmarks: c.bookmarks,
	}
	data, err := json.MarshalIndent(payload, "", "  ")
	if err != nil {
		return fmt.Errorf("сериализация JSON: %w", err)
	}
	if err := os.WriteFile(c.path, data, 0o600); err != nil {
		return fmt.Errorf("запись файла закладок: %w", err)
	}
	return nil
}

// Add добавляет новую закладку и сразу сохраняет файл.
func (c *FileCatalog) Add(title, rawURL string, tags []string) (Bookmark, error) {
	cleanTitle := strings.TrimSpace(title)
	cleanURL := strings.TrimSpace(rawURL)
	if cleanTitle == "" {
		return Bookmark{}, ErrEmptyTitle
	}
	if !strings.HasPrefix(cleanURL, "http://") && !strings.HasPrefix(cleanURL, "https://") {
		return Bookmark{}, fmt.Errorf("%w: %q", ErrInvalidURL, cleanURL)
	}

	bm := Bookmark{
		ID:        c.nextID,
		Title:     cleanTitle,
		URL:       cleanURL,
		Tags:      normalizeTags(tags),
		CreatedAt: time.Now().UTC().Truncate(time.Second),
	}
	c.nextID++
	c.bookmarks = append(c.bookmarks, bm)
	if err := c.Save(); err != nil {
		return Bookmark{}, err
	}
	return bm, nil
}

// List возвращает копию всех закладок.
func (c *FileCatalog) List() []Bookmark {
	out := make([]Bookmark, len(c.bookmarks))
	for i, bm := range c.bookmarks {
		bm.Tags = slices.Clone(bm.Tags)
		out[i] = bm
	}
	return out
}

// Delete удаляет закладку по ID и сохраняет файл.
func (c *FileCatalog) Delete(id int) error {
	idx := slices.IndexFunc(c.bookmarks, func(b Bookmark) bool { return b.ID == id })
	if idx == -1 {
		return fmt.Errorf("%w: #%d", ErrNotFound, id)
	}
	c.bookmarks = slices.Delete(c.bookmarks, idx, idx+1)
	return c.Save()
}

func normalizeTags(tags []string) []string {
	var clean []string
	for _, t := range tags {
		tag := strings.ToLower(strings.TrimSpace(t))
		if tag != "" && !slices.Contains(clean, tag) {
			clean = append(clean, tag)
		}
	}
	slices.Sort(clean)
	return clean
}
