package step04

import (
	"errors"
	"path/filepath"
	"testing"
)

func TestStoreImplementations(t *testing.T) {
	t.Run("MemoryStore", func(t *testing.T) {
		runStoreContract(t, NewMemoryStore())
	})

	t.Run("FileStore", func(t *testing.T) {
		path := filepath.Join(t.TempDir(), "store.json")
		fs, err := OpenFileStore(path)
		if err != nil {
			t.Fatalf("OpenFileStore failed: %v", err)
		}
		runStoreContract(t, fs)
	})
}

func runStoreContract(t *testing.T, s Store) {
	t.Helper()

	bm1, err := s.Create(Bookmark{Title: "Go Tour", URL: "https://go.dev/tour", Tags: []string{"Go", "learning"}})
	if err != nil {
		t.Fatalf("Create failed: %v", err)
	}
	if bm1.ID != 1 {
		t.Fatalf("got ID %d, want 1", bm1.ID)
	}

	got, err := s.Get(bm1.ID)
	if err != nil {
		t.Fatalf("Get failed: %v", err)
	}
	if got.Title != "Go Tour" {
		t.Fatalf("got title %q, want %q", got.Title, "Go Tour")
	}

	got.Title = "A Tour of Go"
	updated, err := s.Update(got)
	if err != nil {
		t.Fatalf("Update failed: %v", err)
	}
	if updated.Title != "A Tour of Go" {
		t.Fatalf("got updated title %q", updated.Title)
	}

	found, err := s.Search("learning")
	if err != nil || len(found) != 1 {
		t.Fatalf("Search by tag got %d items, err=%v", len(found), err)
	}

	if err := s.Delete(bm1.ID); err != nil {
		t.Fatalf("Delete failed: %v", err)
	}
	if _, err := s.Get(bm1.ID); !errors.Is(err, ErrNotFound) {
		t.Fatalf("Get after delete got err=%v, want ErrNotFound", err)
	}
}
