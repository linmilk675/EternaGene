from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import string

# Главное меню
def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📋 Показать гены старения", callback_data="show_genes")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_letter_keyboard():
    keyboard = []
    row = []
    for i, letter in enumerate(string.ascii_uppercase):
        row.append(InlineKeyboardButton(letter, callback_data=f"letter_{letter}"))
        if (i + 1) % 6 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

# Клавиатура генов на букву
def get_genes_by_letter_keyboard(genes, letter, row_size=2):
    keyboard = []
    row = []
    for i, gene in enumerate(genes):
        row.append(InlineKeyboardButton(gene, callback_data=f"select_gene:{gene}"))
        if (i + 1) % row_size == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("⬅️ Назад к буквам", callback_data="back_to_letters")])
    return InlineKeyboardMarkup(keyboard)

# Назад к буквам
def get_back_to_letter_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад к буквам", callback_data="back_to_letters")]
    ])

# Назад к генам на выбранную букву
def get_back_to_genes_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад к списку генов", callback_data="back_to_genes")]
    ])

# Назад к базам данных гена
def get_back_to_gene_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад к меню гена", callback_data="back_to_gene_menu")]
    ])

def get_back_to_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Вернуться в главное меню", callback_data="back_to_main")]
    ])

# Меню баз данных для аннотаций гена
def get_database_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🧬 NCBI", callback_data="db_ncbi"),
            InlineKeyboardButton("🧬 Ensembl", callback_data="db_ensembl"),
        ],
        [
            InlineKeyboardButton("🧬 UniProt", callback_data="db_uniprot"),
            #InlineKeyboardButton("🧬 GeneCards", callback_data="db_genecards"),
        ],
        [
            #InlineKeyboardButton("🧬 AllianceGenome", callback_data="db_alliance"),
        ],
        [
            InlineKeyboardButton("🔗 Показать взаимодействия", callback_data="show_interactions"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_interaction_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📊 Построить граф взаимодействий", callback_data="show_graph"),
        ],
        [
            InlineKeyboardButton("⬅️ Назад", callback_data="back_to_gene_menu"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
