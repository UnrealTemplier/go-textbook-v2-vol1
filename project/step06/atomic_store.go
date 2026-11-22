package step06

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"slices"
	"sync"
)

var ErrNotFound = errors.New("закладка не найдена")

// Bookmark описывает запись в файловом хранилище.
type Bookmark struct {
	ID    int    `json:"id"`
	Title string `json:"title"`
	URL   string `json:"url"`
}

// WriteFileAtomic безопасно перезаписывает файл через временный файл в том же каталоге и os.Rename.
func WriteFileAtomic(path string, data []byte) error {
	dir := filepath.Dir(path)
	tmp, err := os.CreateTemp(dir, ".bookmarkflow-*.tmp")
	if err != nil {
		return fmt.Errorf("создание временного файла: %w", err)
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
		return fmt.Errorf("запись временного файла: %w", err)
	}
	if err := tmp.Sync(); err != nil {
		_ = tmp.Close()
		return fmt.Errorf("синхронизация на диск: %w", err)
	}
	if err := tmp.Close(); err != nil {
		return fmt.Errorf("закрытие временного файла: %w", err)
	}
	if err := os.Rename(tmpName, path); err != nil {
		return fmt.Errorf("атомарное переименование: %w", err)
	}
	cleanup = false
	return nil
}

// AtomicStore хранит закладки в памяти и атомарно сбрасывает их в JSON-файл.
type AtomicStore struct {
	mu     sync.RWMutex
	path   string
	nextID int
	items  []Bookmark
}

type snapshot struct {
	NextID int        `json:"next_id"`
	Items  []Bookmark `json:"items"`
}

// OpenAtomicStore загружает существующий JSON-файл или создаёт новое хранилище.
func OpenAtomicStore(path string) (*AtomicStore, error) {
	s := &AtomicStore{path: path, nextID: 1}
	data, err := os.ReadFile(path)
	if errors.Is(err, os.ErrNotExist) {
		return s, nil
	}
	if err != nil {
		return nil, err
	}
	if len(data) == 0 {
		return s, nil
	}
	var snap snapshot
	if err := json.Unmarshal(data, &snap); err != nil {
		return nil, err
	}
	s.nextID = max(snap.NextID, 1)
	s.items = snap.Items
	return s, nil
}

func (s *AtomicStore) Add(title, rawURL string) (Bookmark, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	bm := Bookmark{ID: s.nextID, Title: title, URL: rawURL}
	s.nextID++
	s.items = append(s.items, bm)
	if err := s.flushLocked(); err != nil {
		return Bookmark{}, err
	}
	return bm, nil
}

func (s *AtomicStore) Get(id int) (Bookmark, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	for _, it := range s.items {
		if it.ID == id {
			return it, nil
		}
	}
	return Bookmark{}, ErrNotFound
}

func (s *AtomicStore) List() []Bookmark {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return slices.Clone(s.items)
}

func (s *AtomicStore) flushLocked() error {
	data, err := json.MarshalIndent(snapshot{NextID: s.nextID, Items: s.items}, "", "  ")
	if err != nil {
		return err
	}
	return WriteFileAtomic(s.path, data)
}
