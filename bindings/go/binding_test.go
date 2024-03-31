package tree_sitter_rst2_test

import (
	"testing"

	tree_sitter "github.com/smacker/go-tree-sitter"
	"github.com/tree-sitter/tree-sitter-rst2"
)

func TestCanLoadGrammar(t *testing.T) {
	language := tree_sitter.NewLanguage(tree_sitter_rst2.Language())
	if language == nil {
		t.Errorf("Error loading Rst grammar")
	}
}
