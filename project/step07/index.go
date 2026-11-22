package step07

import (
	"cmp"
	"slices"
	"strings"
)

// Bookmark представляет закладку для индексации и поиска.
type Bookmark struct {
	ID    int
	Title string
	URL   string
	Tags  []string
}

// TagIndex строит инвертированный индекс «тег -> отсортированный список ID закладок».
// Поиск по одному тегу занимает O(1) для доступа к списку ID, пересечение двух тегов — O(k1 + k2).
type TagIndex struct {
	byTag map[string][]int
}

// NewTagIndex создаёт пустой инвертированный индекс.
func NewTagIndex() *TagIndex {
	return &TagIndex{byTag: make(map[string][]int)}
}

// Index индексирует все теги закладки.
func (idx *TagIndex) Index(b Bookmark) {
	for _, raw := range b.Tags {
		tag := strings.ToLower(strings.TrimSpace(raw))
		if tag == "" {
			continue
		}
		ids := idx.byTag[tag]
		pos, found := slices.BinarySearch(ids, b.ID)
		if !found {
			idx.byTag[tag] = slices.Insert(ids, pos, b.ID)
		}
	}
}

// Remove удаляет закладку из индекса по её ID и тегам.
func (idx *TagIndex) Remove(id int, tags []string) {
	for _, raw := range tags {
		tag := strings.ToLower(strings.TrimSpace(raw))
		ids := idx.byTag[tag]
		pos, found := slices.BinarySearch(ids, id)
		if !found {
			continue
		}
		ids = slices.Delete(ids, pos, pos+1)
		if len(ids) == 0 {
			delete(idx.byTag, tag)
		} else {
			idx.byTag[tag] = ids
		}
	}
}

// FindByTag возвращает копию отсортированного списка ID закладок с указанным тегом.
func (idx *TagIndex) FindByTag(tag string) []int {
	key := strings.ToLower(strings.TrimSpace(tag))
	return slices.Clone(idx.byTag[key])
}

// FindByAllTags возвращает ID закладок, у которых есть все перечисленные теги.
func (idx *TagIndex) FindByAllTags(tags ...string) []int {
	if len(tags) == 0 {
		return nil
	}
	res := idx.FindByTag(tags[0])
	for _, raw := range tags[1:] {
		res = intersectSorted(res, idx.FindByTag(raw))
		if len(res) == 0 {
			return nil
		}
	}
	return res
}

// intersectSorted находит пересечение двух отсортированных слайсов методом двух указателей за O(n + m).
func intersectSorted(a, b []int) []int {
	var out []int
	i, j := 0, 0
	for i < len(a) && j < len(b) {
		switch cmp.Compare(a[i], b[j]) {
		case -1:
			i++
		case 1:
			j++
		case 0:
			out = append(out, a[i])
			i++
			j++
		}
	}
	return out
}

// BinarySearchByID ищет закладку по ID в слайсе, отсортированном по возрастанию ID, за O(log n).
func BinarySearchByID(sorted []Bookmark, id int) (Bookmark, bool) {
	lo, hi := 0, len(sorted)-1
	for lo <= hi {
		mid := lo + (hi-lo)/2
		switch cmp.Compare(sorted[mid].ID, id) {
		case 0:
			return sorted[mid], true
		case -1:
			lo = mid + 1
		case 1:
			hi = mid - 1
		}
	}
	return Bookmark{}, false
}

// SortByTitle возвращает новую копию слайса, отсортированную по названию (без учёта регистра) и ID.
func SortByTitle(items []Bookmark) []Bookmark {
	out := slices.Clone(items)
	slices.SortFunc(out, func(a, b Bookmark) int {
		if c := cmp.Compare(strings.ToLower(a.Title), strings.ToLower(b.Title)); c != 0 {
			return c
		}
		return cmp.Compare(a.ID, b.ID)
	})
	return out
}
