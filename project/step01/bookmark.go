package step01

import (
	"errors"
	"fmt"
	"io"
	"strings"
)

var (
	// ErrEmptyTitle возвращается, если название закладки пустое.
	ErrEmptyTitle = errors.New("название закладки не может быть пустым")
	// ErrInvalidURL возвращается, если адрес не начинается с http:// или https://.
	ErrInvalidURL = errors.New("ссылка должна начинаться с http:// или https://")
)

// ValidateInputs проверяет название и URL закладки до добавления.
func ValidateInputs(title, rawURL string) (string, string, error) {
	cleanTitle := strings.TrimSpace(title)
	cleanURL := strings.TrimSpace(rawURL)
	if cleanTitle == "" {
		return "", "", ErrEmptyTitle
	}
	if !strings.HasPrefix(cleanURL, "http://") && !strings.HasPrefix(cleanURL, "https://") {
		return "", "", fmt.Errorf("%w: %q", ErrInvalidURL, cleanURL)
	}
	return cleanTitle, cleanURL, nil
}

// AddBookmark добавляет проверенную закладку в параллельные списки названий и ссылок.
func AddBookmark(titles, urls []string, title, rawURL string) ([]string, []string, error) {
	cleanTitle, cleanURL, err := ValidateInputs(title, rawURL)
	if err != nil {
		return titles, urls, err
	}
	return append(titles, cleanTitle), append(urls, cleanURL), nil
}

// FormatLine форматирует одну строку списка закладок для вывода в терминал.
func FormatLine(id int, title, rawURL string) string {
	return fmt.Sprintf("#%d | %s -> %s", id, title, rawURL)
}

// PrintList печатает все закладки в переданный поток вывода.
func PrintList(w io.Writer, titles, urls []string) error {
	if len(titles) == 0 {
		_, err := fmt.Fprintln(w, "Список закладок пуст.")
		return err
	}
	for i := range len(titles) {
		if _, err := fmt.Fprintln(w, FormatLine(i+1, titles[i], urls[i])); err != nil {
			return err
		}
	}
	return nil
}
