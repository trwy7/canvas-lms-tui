package main

import (
	"fmt"
	"log"
	"os"

	"github.com/charmbracelet/bubbles/list"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// Messages to print after we quit (like what we did)

var finalmsg = []string{}

// The create a struct for serverItem
type serverItem struct {
	name, url string
}

func (i serverItem) Title() string       { return i.name }
func (i serverItem) Description() string { return i.url }
func (i serverItem) FilterValue() string { return i.name }

// Create the UI stuff
var docStyle = lipgloss.NewStyle().Margin(1, 2)

type model struct {
	list     list.Model
	choice   string
	quitting bool
}

func (m model) Init() tea.Cmd {
	return nil
}

// Update function

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		if msg.String() == "ctrl+c" {
			m.quitting = true
			return m, tea.Quit
		}
		if msg.String() == "enter" {
			i, ok := m.list.SelectedItem().(serverItem)
			if ok {
				m.choice = i.url
			}
			return m, tea.Quit
		}
	case tea.WindowSizeMsg:
		h, v := docStyle.GetFrameSize()
		m.list.SetSize(msg.Width-h, msg.Height-v)
	}

	var cmd tea.Cmd
	m.list, cmd = m.list.Update(msg)
	return m, cmd
}

// Create the view

func (m model) View() string {
	if m.choice != "" {
		return fmt.Sprintf("\nSelected: %s\n", m.choice)
	}
	if m.quitting {
		return "\nGoodbye!\n"
	}
	return docStyle.Render(m.list.View())
}

func main() {
	// Get config
	serverConfig, err := load_data("servers.json")
	if err != nil {
		log.Fatal(err)
	}
	// Create a list for the modal
	items := []list.Item{}
	for _, s := range serverConfig {
		items = append(items, serverItem{name: s["name"], url: s["url"]})
	}
	// Set up the modal
	m := model{list: list.New(items, list.NewDefaultDelegate(), 0, 0)}
	m.list.Title = "Select an instance"

	p := tea.NewProgram(m, tea.WithAltScreen())

	if _, err := p.Run(); err != nil {
		fmt.Println("Error running program:", err)
		os.Exit(1)
	}
}
