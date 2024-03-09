from graphviz import Digraph

class RegularExpression:
    def __init__(self, value):
        self.value = value

class Action:
    def __init__(self, value):
        self.value = value

class TokenDefinition:
    def __init__(self, name, regexp, action):
        self.name = name
        self.regexp = regexp
        self.action = action
        self.children = []

class TreeNode:
    latest_id = 0
    tree_graph = Digraph(format='png')

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

        TreeNode.latest_id += 1
        self.id = TreeNode.latest_id

    def make_tree(self):
        # Método para construir el árbol de expresión
        if self.left:
            TreeNode.tree_graph.edge(self.value, self.left.value)
            self.left.make_tree()

        if self.right:
            TreeNode.tree_graph.edge(self.value, self.right.value)
            self.right.make_tree()

    @staticmethod
    def _render_tree():
        # Método para renderizar el árbol de expresión
        TreeNode.tree_graph.render('out/expression_tree', view=True)

    def print_tree(self):
        # Método para imprimir el árbol de expresión
        TreeNode.tree_graph.graph_attr['rankdir'] = 'TB'  # Opcional: para orientar el árbol verticalmente
        TreeNode.tree_graph.node(self.value, shape='plaintext')  # Especificamos que los nodos son de forma plaintext
        self.make_tree()
        self._render_tree()


class YALexLexer:
    def __init__(self, filename):
        self.filename = filename
        self.tokens = []

    def tokenize(self):
        # Método para tokenizar el archivo lexer.yal
        with open(self.filename, 'r') as file:
            content = file.read()

            # Dividir el contenido en secciones
            sections = self._split_sections(content)

            # Analizar cada sección
            for section in sections:
                self._parse_section(section)

    def _split_sections(self, content):
        # Método para dividir el contenido del archivo en secciones
        sections = []
        current_section = []
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                # Agregar la sección actual a la lista de secciones
                if current_section:
                    sections.append('\n'.join(current_section))
                    current_section = []
            else:
                # Agregar la línea actual a la sección actual
                current_section.append(line)
        # Agregar la última sección (si existe)
        if current_section:
            sections.append('\n'.join(current_section))
        return sections

    def _parse_section(self, section):
        # Método para analizar una sección específica del archivo YALex
        # Dividimos la sección en líneas y eliminamos las líneas en blanco
        lines = [line.strip() for line in section.split('\n') if line.strip()]

        if lines:
            # La primera línea define el nombre del token
            token_name = lines[0]

            # Las líneas restantes contienen expresiones regulares y acciones
            for line in lines[1:]:
                # Ignorar líneas que contienen comentarios de tipo (* *)
                if '(*' in line and '*)' in line:
                    continue

                # Dividir la línea en expresión regular y acción (si existe)
                parts = line.split('{', 1)
                regexp = RegularExpression(parts[0].strip())
                action = Action(parts[1].split('}')[0].strip()) if len(parts) > 1 else None

                # Agregar el token analizado a la lista
                self.tokens.append(TokenDefinition(token_name, regexp, action))

    def build_expression_tree(self):
        # Método para construir el árbol de expresión
        root = TreeNode('Root')
        for token in self.tokens:
            current_node = root
            for char in token.regexp.value:
                found = False
                if char == '"':
                    char = r'\"'  # Manejar la comilla doble escapada
                elif char == '\\':
                    char = r'\\'  # Manejar la barra invertida escapada
                if current_node.left and current_node.left.value == char:
                    current_node = current_node.left
                    found = True
                elif current_node.right and current_node.right.value == char:
                    current_node = current_node.right
                    found = True
                if not found:
                    new_node = TreeNode(char)
                    if current_node.left is None:
                        current_node.left = new_node
                    else:
                        current_node.right = new_node
                    current_node = new_node
        return root

    def display_tokens(self):
        # Método para mostrar los tokens
        for token in self.tokens:
            print("Token:", token.name)
            print("Regular Expression:", token.regexp.value)
            print("Action:", token.action.value if token.action else None)
            print()

# Crear una instancia de YALexLexer y realizar el análisis léxico
lexer = YALexLexer('lexer.yal')
lexer.tokenize()
# Mostrar los tokens extraídos del archivo
lexer.display_tokens()
# Construir y mostrar el árbol de expresión
tree_root = lexer.build_expression_tree()
tree_root.print_tree()
