package step02

import (
	"errors"
	"fmt"
	"io"
	"strconv"
	"strings"
)

var (
	ErrEmptyTitle     = errors.New("название закладки не может быть пустым")
	ErrInvalidURL     = errors.New("ссылка должна начинаться с http:// или https://")
	ErrNotFound       = errors.New("закладка не найдена")
	ErrUnknownCommand = errors.New("неизвестная команда")
	ErrInvalidArgs    = errors.New("некорректные аргументы команды")
)

type item struct {
	id    int
	title string
	url   string
}

// App хранит состояние CLI-менеджера закладок в памяти.
type App struct {
	nextID int
	items  []item
}

// NewApp создаёт пустое приложение BookmarkFlow.
func NewApp() *App {
	return &App{nextID: 1}
}

// Execute разбирает и выполняет консольную команду: add, list, search, delete.
func (a *App) Execute(args []string, out io.Writer) error {
	if len(args) == 0 {
		return fmt.Errorf("%w: укажите команду (add, list, search, delete)", ErrInvalidArgs)
	}

	switch args[0] {
	case "add":
		if len(args) != 3 {
			return fmt.Errorf("%w: формат add <название> <url>", ErrInvalidArgs)
		}
		id, err := a.Add(args[1], args[2])
		if err != nil {
			return err
		}
		_, err = fmt.Fprintf(out, "Добавлена закладка #%d\n", id)
		return err

	case "list":
		return writeTable(out, a.items)

	case "search":
		if len(args) != 2 {
			return fmt.Errorf("%w: формат search <запрос>", ErrInvalidArgs)
		}
		matches := a.Search(args[1])
		return writeTable(out, matches)

	case "delete":
		if len(args) != 2 {
			return fmt.Errorf("%w: формат delete <id>", ErrInvalidArgs)
		}
		id, err := strconv.Atoi(args[1])
		if err != nil || id <= 0 {
			return fmt.Errorf("%w: некорректный id %q", ErrInvalidArgs, args[1])
		}
		if err := a.Delete(id); err != nil {
			return err
		}
		_, err = fmt.Fprintf(out, "Закладка #%d удалена\n", id)
		return err

	default:
		return fmt.Errorf("%w: %q", ErrUnknownCommand, args[0])
	}
}

// Add проверяет поля и добавляет закладку в память.
func (a *App) Add(title, rawURL string) (int, error) {
	cleanTitle := strings.TrimSpace(title)
	cleanURL := strings.TrimSpace(rawURL)
	if cleanTitle == "" {
		return 0, ErrEmptyTitle
	}
	if !strings.HasPrefix(cleanURL, "http://") && !strings.HasPrefix(cleanURL, "https://") {
		return 0, fmt.Errorf("%w: %q", ErrInvalidURL, cleanURL)
	}
	id := a.nextID
	a.nextID++
	a.items = append(a.items, item{id: id, title: cleanTitle, url: cleanURL})
	return id, nil
}

// Search ищет закладки по подстроке в названии или URL без учёта регистра.
func (a *App) Search(query string) []item {
	q := strings.ToLower(strings.TrimSpace(query))
	if q == "" {
		return append([]item(nil), a.items...)
	}
	var res []item
	for _, it := range a.items {
		if strings.Contains(strings.ToLower(it.title), q) || strings.Contains(strings.ToLower(it.url), q) {
			res = append(res, it)
		}
	}
	return res
}

// Delete удаляет закладку по идентификатору.
func (a *App) Delete(id int) error {
	for i, it := range a.items {
		if it.id == id {
			a.items = append(a.items[:i], a.items[i+1:]...)
			return nil
		}
	}
	return fmt.Errorf("%w: #%d", ErrNotFound, id)
}

func writeTable(w io.Writer, items []item) error {
	if len(items) == 0 {
		_, err := fmt.Fprintln(w, "Ничего не найдено.")
		return err
	}
	for _, it := range items {
		if _, err := fmt.Fprintf(w, "%-4d | %-24s | %s\n", it.id, it.title, it.url); err != nil {
			return err
		}
	}
	return nil
}
