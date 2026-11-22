package step06

import (
	"bufio"
	"fmt"
	"net"
	"path/filepath"
	"strings"
	"testing"
)

func TestAtomicStoreAndTCPProtocol(t *testing.T) {
	storePath := filepath.Join(t.TempDir(), "bookmarks.json")
	store, err := OpenAtomicStore(storePath)
	if err != nil {
		t.Fatalf("OpenAtomicStore failed: %v", err)
	}
	if _, err := store.Add("GoDoc", "https://pkg.go.dev"); err != nil {
		t.Fatalf("Add failed: %v", err)
	}

	// Убедимся, что атомарная запись пережила повторное открытие.
	reloaded, err := OpenAtomicStore(storePath)
	if err != nil {
		t.Fatalf("reload failed: %v", err)
	}
	if len(reloaded.List()) != 1 {
		t.Fatalf("expected 1 bookmark after reload, got %d", len(reloaded.List()))
	}

	srv, err := StartTCPServer("127.0.0.1:0", reloaded)
	if err != nil {
		t.Fatalf("StartTCPServer failed: %v", err)
	}
	defer func() {
		if err := srv.Close(); err != nil {
			t.Errorf("Close failed: %v", err)
		}
	}()

	conn, err := net.Dial("tcp", srv.Addr())
	if err != nil {
		t.Fatalf("Dial failed: %v", err)
	}
	defer conn.Close()

	reader := bufio.NewReader(conn)
	send := func(cmd string) string {
		t.Helper()
		if _, err := fmt.Fprintln(conn, cmd); err != nil {
			t.Fatalf("write %q failed: %v", cmd, err)
		}
		resp, err := reader.ReadString('\n')
		if err != nil {
			t.Fatalf("read after %q failed: %v", cmd, err)
		}
		return strings.TrimSpace(resp)
	}

	if got := send("PING"); got != "PONG" {
		t.Fatalf("PING got %q, want PONG", got)
	}
	if got := send("COUNT"); got != "COUNT 1" {
		t.Fatalf("COUNT got %q, want COUNT 1", got)
	}
	if got := send("GET 1"); got != "OK 1 GoDoc https://pkg.go.dev" {
		t.Fatalf("GET 1 got %q", got)
	}
	if got := send("GET 99"); got != "ERR not found" {
		t.Fatalf("GET 99 got %q, want ERR not found", got)
	}
	if got := send("QUIT"); got != "BYE" {
		t.Fatalf("QUIT got %q, want BYE", got)
	}
}
