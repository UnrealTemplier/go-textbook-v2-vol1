package step03

import (
	"errors"
	"path/filepath"
	"slices"
	"testing"
)

func TestFileCatalogPersistence(t *testing.T) {
	filePath := filepath.Join(t.TempDir(), "bookmarks.json")

	cat, err := OpenFileCatalog(filePath)
	if err != nil {
		t.Fatalf("OpenFileCatalog failed: %v", err)
	}

	added, err := cat.Add("Go Effective", "https://go.dev/doc/effective_go", []string{"Go", "docs", "go"})
	if err != nil {
		t.Fatalf("Add failed: %v", err)
	}
	if added.ID != 1 {
		t.Fatalf("got ID %d, want 1", added.ID)
	}
	if !slices.Equal(added.Tags, []string{"docs", "go"}) {
		t.Fatalf("got tags %v, want [docs go]", added.Tags)
	}

	// Повторно открываем каталог с диска и убеждаемся, что данные сохранились.
	reloaded, err := OpenFileCatalog(filePath)
	if err != nil {
		t.Fatalf("reload failed: %v", err)
	}
	items := reloaded.List()
	if len(items) != 1 || items[0].Title != "Go Effective" {
		t.Fatalf("unexpected reloaded items: %+v", items)
	}

	if err := reloaded.Delete(added.ID); err != nil {
		t.Fatalf("Delete failed: %v", err)
	}
	if err := reloaded.Delete(added.ID); !errors.Is(err, ErrNotFound) {
		t.Fatalf("got err %v, want ErrNotFound", err)
	}
}
