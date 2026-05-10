import streamlit as st
import database
import time

st.set_page_config(page_title="Smart Voice Notes", layout="wide")

# --- ЛОГИКА АВТОРИЗАЦИИ ЧЕРЕЗ URL ---
# Проверяем, есть ли ID в ссылке (например, ?u=12345)
if "u" in st.query_params:
    st.session_state.u_id = int(st.query_params["u"])

# Если ID нет в сессии, просим ввести вручную (только один раз)
if "u_id" not in st.session_state:
    st.sidebar.title("🔑 Вход")
    u_id_input = st.sidebar.number_input("Введите ваш Telegram ID", step=1, value=0)
    if u_id_input > 0:
        st.session_state.u_id = u_id_input
        st.rerun()

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
if "u_id" in st.session_state:
    u_id = st.session_state.u_id
    st.title(f"🗒 Мои заметки (ID: {u_id})")
    
    # Кнопка выхода в сайдбаре
    if st.sidebar.button("Выйти / Сменить ID"):
        del st.session_state.u_id
        st.query_params.clear()
        st.rerun()

    # --- ФРАГМЕНТ ДЛЯ АВТО-ОБНОВЛЕНИЯ СПИСКА ---
    @st.fragment(run_every=30) # Обновляет этот блок каждые 30 секунд
    def show_notes():
        try:
            response = database.fetch_notes(u_id)
            notes = response.data

            if not notes:
                st.info("Заметок пока нет. Отправьте голосовое боту!")
                return

            # Фильтрация по тегам
            all_tags = set()
            for n in notes: all_tags.update(n['tags'])
            
            tag_filter = st.multiselect("🔍 Фильтр по темам", sorted(list(all_tags)))
            
            # Сортировка и отображение
            for n in notes:
                if tag_filter and not any(t in n['tags'] for t in tag_filter):
                    continue
                
                with st.expander(f"📌 {n['title']} — {n['created_at'][11:16]} ({n['created_at'][:10]})"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Суть:** {n['summary']}")
                    with col2:
                        # Кнопка для удаления (опционально)
                        if st.button("🗑 Удалить", key=f"del_{n['id']}"):
                            database.supabase.table("notes").delete().eq("id", n['id']).execute()
                            st.rerun()

                    st.audio(n['file_url'])
                    st.text_area("Полная расшифровка", n['raw_text'], height=150, key=f"txt_{n['id']}")
                    st.caption(f"🏷 {', '.join(n['tags'])}")

        except Exception as e:
            st.error(f"Ошибка загрузки: {e}")

    # Запуск отображения
    show_notes()

else:
    st.info("👋 Пожалуйста, введите ваш Telegram ID или перейдите по ссылке из бота.")
    st.image("https://via.placeholder.com/800x400.png?text=Smart+Voice+Notes+Waiting...") # Заглушка