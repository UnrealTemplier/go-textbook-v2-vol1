package step05

import (
	"context"
	"log/slog"
	"slices"
	"sync"
	"time"
)

// Bookmark представляет закладку для проверки доступности.
type Bookmark struct {
	ID    int
	Title string
	URL   string
}

// ProbeResult хранит итог проверки одной ссылки.
type ProbeResult struct {
	BookmarkID int
	URL        string
	OK         bool
	Latency    time.Duration
	Err        error
}

// Prober проверяет доступность URL с учётом отмены контекста.
type Prober func(ctx context.Context, rawURL string) (bool, error)

// SafeStore обеспечивает потокобезопасный доступ к закладкам через sync.RWMutex.
type SafeStore struct {
	mu     sync.RWMutex
	nextID int
	items  []Bookmark
}

// NewSafeStore создаёт пустое потокобезопасное хранилище.
func NewSafeStore() *SafeStore {
	return &SafeStore{nextID: 1}
}

// Add безопасно добавляет закладку из любой горутины.
func (s *SafeStore) Add(title, rawURL string) Bookmark {
	s.mu.Lock()
	defer s.mu.Unlock()
	bm := Bookmark{ID: s.nextID, Title: title, URL: rawURL}
	s.nextID++
	s.items = append(s.items, bm)
	return bm
}

// List возвращает независимый снимок всех закладок.
func (s *SafeStore) List() []Bookmark {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return slices.Clone(s.items)
}

// CheckAll конкурентно проверяет список закладок пулом из workers воркеров.
// Порядок результатов совпадает с порядком входного слайса bookmarks.
func CheckAll(
	ctx context.Context,
	bookmarks []Bookmark,
	workers int,
	probe Prober,
	logger *slog.Logger,
) []ProbeResult {
	if len(bookmarks) == 0 {
		return nil
	}
	workers = max(workers, 1)
	workers = min(workers, len(bookmarks))
	if logger == nil {
		logger = slog.New(slog.DiscardHandler)
	}

	type job struct {
		idx int
		bm  Bookmark
	}

	jobs := make(chan job)
	results := make([]ProbeResult, len(bookmarks))

	var wg sync.WaitGroup
	for range workers {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := range jobs {
				start := time.Now()
				ok, err := probe(ctx, j.bm.URL)
				res := ProbeResult{
					BookmarkID: j.bm.ID,
					URL:        j.bm.URL,
					OK:         ok,
					Latency:    time.Since(start),
					Err:        err,
				}
				results[j.idx] = res
				logger.Info("проверка закладки завершена",
					slog.Int("id", j.bm.ID),
					slog.String("url", j.bm.URL),
					slog.Bool("ok", ok),
				)
			}
		}()
	}

	for i, bm := range bookmarks {
		select {
		case <-ctx.Done():
			results[i] = ProbeResult{
				BookmarkID: bm.ID,
				URL:        bm.URL,
				OK:         false,
				Err:        ctx.Err(),
			}
		case jobs <- job{idx: i, bm: bm}:
		}
	}
	close(jobs)
	wg.Wait()

	return results
}
