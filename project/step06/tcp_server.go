package step06

import (
	"bufio"
	"errors"
	"fmt"
	"net"
	"strconv"
	"strings"
	"sync"
)

// TCPServer обслуживает простой текстовый протокол поверх TCP:
// PING, COUNT, LIST, GET <id>, QUIT.
type TCPServer struct {
	store *AtomicStore
	ln    net.Listener
	wg    sync.WaitGroup
}

// StartTCPServer запускает TCP-сервер на указанном адресе (например "127.0.0.1:0").
func StartTCPServer(addr string, store *AtomicStore) (*TCPServer, error) {
	ln, err := net.Listen("tcp", addr)
	if err != nil {
		return nil, err
	}
	srv := &TCPServer{store: store, ln: ln}
	srv.wg.Add(1)
	go srv.acceptLoop()
	return srv, nil
}

// Addr возвращает фактический адрес прослушивания.
func (s *TCPServer) Addr() string {
	return s.ln.Addr().String()
}

// Close останавливает приём новых соединений и ждёт завершения активных обработчиков.
func (s *TCPServer) Close() error {
	err := s.ln.Close()
	s.wg.Wait()
	return err
}

func (s *TCPServer) acceptLoop() {
	defer s.wg.Done()
	for {
		conn, err := s.ln.Accept()
		if err != nil {
			if errors.Is(err, net.ErrClosed) {
				return
			}
			continue
		}
		s.wg.Add(1)
		go func() {
			defer s.wg.Done()
			defer conn.Close()
			s.handleConn(conn)
		}()
	}
}

func (s *TCPServer) handleConn(conn net.Conn) {
	scanner := bufio.NewScanner(conn)
	writer := bufio.NewWriter(conn)

	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		fields := strings.Fields(line)
		cmd := strings.ToUpper(fields[0])

		switch cmd {
		case "PING":
			_, _ = fmt.Fprintln(writer, "PONG")
		case "COUNT":
			_, _ = fmt.Fprintf(writer, "COUNT %d\n", len(s.store.List()))
		case "LIST":
			items := s.store.List()
			for _, it := range items {
				_, _ = fmt.Fprintf(writer, "%d %s %s\n", it.ID, it.Title, it.URL)
			}
			_, _ = fmt.Fprintln(writer, "END")
		case "GET":
			if len(fields) != 2 {
				_, _ = fmt.Fprintln(writer, "ERR usage: GET <id>")
				break
			}
			id, err := strconv.Atoi(fields[1])
			if err != nil {
				_, _ = fmt.Fprintln(writer, "ERR invalid id")
				break
			}
			bm, err := s.store.Get(id)
			if err != nil {
				_, _ = fmt.Fprintln(writer, "ERR not found")
				break
			}
			_, _ = fmt.Fprintf(writer, "OK %d %s %s\n", bm.ID, bm.Title, bm.URL)
		case "QUIT":
			_, _ = fmt.Fprintln(writer, "BYE")
			_ = writer.Flush()
			return
		default:
			_, _ = fmt.Fprintf(writer, "ERR unknown command %q\n", cmd)
		}
		_ = writer.Flush()
	}
}
