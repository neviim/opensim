#include <boosd_lexer.h>
#include <boosd_parser.h>
#include <stdlib.h>

typedef pANTLR3_INPUT_STREAM antlr3_input_stream;
typedef pANTLR3_COMMON_TOKEN_STREAM antlr3_common_token_stream;
typedef pANTLR3_COMMON_TREE_NODE_STREAM antlr3_common_tree_node_stream;

typedef boosdLexer boosd_lexer;
#define boosd_lexer_new(instream) boosdLexerNew(instream)

typedef boosdParser boosd_parser;
#define boosd_parser_new(instream) boosdParserNew(instream)

typedef boosdParser_statements_return boosd_parser_statements_return;


typedef unsigned char u8;
typedef char s8;
typedef unsigned short u16;
typedef short s16;

#define antlr3_ascii_file_stream_new antlr3AsciiFileStreamNew

int
main(int argc, const char *argv[])
{

	u8                              *file_name;
	antlr3_input_stream              input;
	boosd_lexer                     *lexer;
	antlr3_common_token_stream       tstream;
	boosd_parser                    *parser;
	boosd_parser_statements_return   langAST;
	antlr3_common_tree_node_stream   nodes;
//	pLangDumpDecl                    boosdParser;

	if (argc < 2 || argv[1] == NULL)
		file_name = (u8 *)"./input";
	else
		file_name = (u8 *)argv[1];

	input = antlr3_ascii_file_stream_new(file_name);
	if (input == NULL)
	{
		fprintf(stderr, "Unable to open file %s due to malloc() failure1\n",
			(char *)file_name);
		exit(1);
	}

	lexer = boosd_lexer_new(input);
	if (lexer == NULL)
	{
		ANTLR3_FPRINTF(stderr, "Unable to create the lexer due to malloc() failure1\n");
		exit(ANTLR3_ERR_NOMEM);
	}

	tstream = antlr3CommonTokenStreamSourceNew(ANTLR3_SIZE_HINT, TOKENSOURCE(lexer));
	if (tstream == NULL)
	{
		ANTLR3_FPRINTF(stderr, "Out of memory trying to allocate token stream\n");
		exit(ANTLR3_ERR_NOMEM);
	}

	parser = boosd_parser_new(tstream);
	if (parser == NULL)
	{
		ANTLR3_FPRINTF(stderr, "Out of memory trying to allocate parser\n");
		exit(ANTLR3_ERR_NOMEM);
	}

	// We are all ready to go. Though that looked complicated at first glance,
	// I am sure, you will see that in fact most of the code above is dealing
	// with errors and there isn;t really that much to do (isn;t this always the
	// case in C? ;-).
	//
	// So, we now invoke the parser. All elements of ANTLR3 generated C components
	// as well as the ANTLR C runtime library itself are pseudo objects. This means
	// that they are represented as pointers to structures, which contain any
	// instance data they need, and a set of pointers to other interfaces or
	// 'methods'. Note that in general, these few pointers we have created here are
	// the only things you will ever explicitly free() as everything else is created
	// via factories, that allocate memory efficiently and free() everything they use
	// automatically when you close the parser/lexer/etc.
	//
	// Note that this means only that the methods are always called via the object
	// pointer and the first argument to any method, is a pointer to the structure itself.
	// It also has the side advantage, if you are using an IDE such as VS2005 that can do it
	// that when you type ->, you will see a list of all the methods the object supports.
	//
	langAST = parser->statements(parser);

	// If the parser ran correctly, we will have a tree to parse. In general I recommend
	// keeping your own flags as part of the error trapping, but here is how you can
	// work out if there were errors if you are using the generic error messages
	//
	if (parser->pParser->rec->getNumberOfSyntaxErrors(parser->pParser->rec) > 0)
	{
		ANTLR3_FPRINTF(stderr, "The parser returned %d errors, tree walking aborted.\n", parser->pParser->rec->getNumberOfSyntaxErrors(parser->pParser->rec));

	}
	else
	{
		nodes   = antlr3CommonTreeNodeStreamNewTree(langAST.tree, ANTLR3_SIZE_HINT); // sIZE HINT WILL SOON BE DEPRECATED!!

		ANTLR3_FPRINTF(stderr, "looks good!!!\n");

		// Tree parsers are given a common tree node stream (or your override)
		//
/*
		boosdParser = donella1ParserNew(nodes);

		boosdParser->statements(boosdParser);

		nodes->free(nodes); nodes = NULL;
		boosdParser->free(boosdParser); boosdParser = NULL;
*/
	}

	// We did not return anything from this parser rule, so we can finish. It only remains
	// to close down our open objects, in the reverse order we created them
	//
	parser->free(parser); parser = NULL;
	tstream->free(tstream); tstream = NULL;
	lexer->free(lexer); lexer = NULL;
	input->close(input); input = NULL;

	return 0;
}
