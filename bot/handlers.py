from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


from bot.keyboards import get_back_to_main_menu_keyboard, get_back_to_gene_menu_keyboard, get_back_to_genes_keyboard, get_letter_keyboard, get_genes_by_letter_keyboard, get_main_menu_keyboard, get_database_menu_keyboard, get_interaction_menu_keyboard

from visualization.gene_network import build_interaction_graph, plot_interaction_graph
from loaders.genage_loader import load_genage_data
from loaders.ncbi_loader import fetch_gene_summary_ncbi
from loaders.ensembl_loader import fetch_ensembl_gene_info
from loaders.uniprot_loader import fetch_uniprot_summary
#from loaders.genecards_loader import fetch_genecards_summary
#from loaders.alliance_loader import fetch_alliance_gene_description
from loaders.string_loader import fetch_string_interactions


# Хранилище выбора пользователя
user_gene_selection = {}
    
# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот для анализа генов, связанных со старением.",
        reply_markup=get_main_menu_keyboard()
    )


# Глобально загружаем гены один раз
genage_df = load_genage_data()
genes_by_letter = {}
for symbol in genage_df["symbol"]:
    letter = symbol[0].upper()
    genes_by_letter.setdefault(letter, []).append(symbol)
    
# Обработка кнопок
async def handle_menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_data = context.user_data

    if query.data == "show_genes":
        await query.edit_message_text("Выберите букву:", reply_markup=get_letter_keyboard())

    elif query.data.startswith("letter_"):
        letter = query.data.split("_")[1]
        user_data["selected_letter"] = letter #сохраняем букву
        genes = genes_by_letter.get(letter.upper(), [])
        if not genes:
            await query.edit_message_text("❌Нет генов на эту букву.")
        else:
            await query.edit_message_text(
                f"🔤 Гены на букву {letter.upper()}:", reply_markup=get_genes_by_letter_keyboard(genes, letter)
            )

    elif query.data.startswith("select_gene:"):
        gene = query.data.split(":")[1]
        context.user_data["selected_gene"] = gene
        await query.edit_message_text(f"✅ Ген {gene} выбран. Выберите базу данных:", reply_markup=get_database_menu_keyboard())
        
    elif query.data.startswith("db_"):
        db = query.data[3:]
        gene = context.user_data.get("selected_gene")
        if not gene:
            await query.edit_message_text("Сначала введите название гена.")
            return
        
        await query.edit_message_text(f"🔎 Запрос в {db.upper()} для гена {gene}...")

        if db == "ncbi":
            data = fetch_gene_summary_ncbi(gene)  # получаем полный словарь
            summary = data.get("Summary", "Summary отсутствует")
        elif db == "ensembl":
            ensembl_data = fetch_ensembl_gene_info(gene)
            summary = ensembl_data.get("description") if ensembl_data else None
        elif db == "uniprot":
            summary = fetch_uniprot_summary(gene)
        #elif db == "genecards":
        #   summary = fetch_genecards_summary(gene)
        #elif db == "alliance":
            # Предположим, ты заранее сопоставил HGNC ID
         #   hgnc_id = f"HGNC:{gene}"  # или из словаря
         #   summary = fetch_alliance_gene_description(hgnc_id)
        else:
            summary = "Неизвестная база."

        await query.message.reply_text(summary or "❗️Аннотация не найдена.", reply_markup=get_back_to_gene_menu_keyboard())
    
    elif query.data == "back_to_letters":
        await query.edit_message_text("🔠 Выберите первую букву гена:", reply_markup=get_letter_keyboard())

    elif query.data == "back_to_genes":
        letter = user_data.get("selected_letter")
        if not letter:
            await query.edit_message_text("Ошибка: буква не выбрана.")
            return
        genes = genes_by_letter.get(letter.upper(), [])
        await query.edit_message_text(
            f"🔤 Гены на букву {letter.upper()}:",
            reply_markup=get_genes_by_letter_keyboard(genes, letter)
        )

    elif query.data == "back_to_gene_menu":
        gene = user_data.get("selected_gene")
        if gene:
            await query.edit_message_text(
                f"✅ Ген {gene} выбран. Выберите базу данных:",
                reply_markup=get_database_menu_keyboard()
            )

    elif query.data == "show_interactions":
        gene = context.user_data.get("selected_gene")
        if not gene:
            await query.edit_message_text("Сначала введите название гена.")
            return
        
        interactions = fetch_string_interactions(gene)
        if not interactions:
            await query.edit_message_text("❌ Взаимодействия не найдены.")
        else:
            text = "\n".join([f"{gene} ↔ {i['partner']} (score: {i['score']})" for i in interactions])
            await query.edit_message_text(f"🔗 Взаимодействия:\n{text}")
            await query.message.reply_text(
            "Что вы хотите сделать дальше?",
            reply_markup=get_interaction_menu_keyboard()
            )

    elif query.data == "back_to_main":
        await query.message.reply_text("🏠 Главное меню:", reply_markup=get_main_menu_keyboard())

    elif query.data == "show_graph":
        gene = context.user_data.get("selected_gene")
        if not gene:
            await query.edit_message_text("Сначала введите название гена.")
            return

        await query.edit_message_text(f"📊 Строим граф взаимодействий для гена {gene}...")

        import os

        G = build_interaction_graph(gene)
        if not G or G.number_of_edges() == 0:
            await query.message.reply_text("❌ Не удалось построить граф — нет взаимодействий.")
            return

        save_path = "data/output_graph.png"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        plot_interaction_graph(G, central_gene=gene, save_path=save_path)

        with open(save_path, "rb") as photo:
            await query.message.reply_photo(photo=photo, caption=f"Граф взаимодействий: {gene}", reply_markup=get_back_to_main_menu_keyboard())

    


# Обработка ввода гена
async def handle_gene_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gene = update.message.text.strip().upper()
    user_gene_selection[update.message.from_user.id] = gene
    await update.message.reply_text(
        f"✅ Ген {gene} выбран. Выбери базу данных:",
        reply_markup=get_database_menu_keyboard()
    )

async def handle_graph_request(update, context):
    gene_name = context.user_data.get("selected_gene")
    if not gene_name:
        await update.message.reply_text("Сначала выберите ген.")
        return

    await update.message.reply_text(f"Строим граф взаимодействий для гена {gene_name}...")

    G = build_interaction_graph(gene_name)
    if not G or G.number_of_edges() == 0:
        await update.message.reply_text("Не удалось построить граф — нет взаимодействий.")
        return

    save_path = "data/output_graph.png"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    plot_interaction_graph(G, central_gene=gene_name, save_path=save_path)

    with open(save_path, "rb") as photo:
        await update.message.reply_photo(photo=photo, caption="Граф взаимодействий")
        
