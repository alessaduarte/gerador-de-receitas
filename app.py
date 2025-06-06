import streamlit as st
import google.generativeai as genai

api_key = st.secrets["API_KEY"]
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel("gemini-2.0-flash")

except Exception as e:
    st.error(f"Erro ao carregar o modelo Gemini 'gemini-2.0-flash': {e}")
    st.info("Verifique se o nome do modelo está correto e se sua chave API tem acesso a ele.")
    st.stop()

def gerar_resposta_gemini(prompt_completo):
    try:
        response = model.generate_content(prompt_completo)

        if response.parts:
            return response.text
        else:
            if response.prompt_feedback:
                st.warning(f"O prompt foi bloqueado. Razão: {response.prompt_feedback.block_reason}")
                if response.prompt_feedback.safety_ratings:
                    for rating in response.prompt_feedback.safety_ratings:
                        st.caption(f"Categoria: {rating.category}, Probabilidade: {rating.probability}")
            return "A IA não pôde gerar uma resposta para este prompt. Verifique as mensagens acima ou tente reformular seu pedido."
    except Exception as e:
        st.error(f"Erro ao gerar resposta da IA: {str(e)}")
        if hasattr(e, 'message'):
            st.error(f"Detalhe da API Gemini: {e.message}")
        return None

st.title("Exercício IA 2: Gerador de Receitas Culinárias Personalizadas com IA")
st.markdown("Recomendações de Receitas")

ingredientes_principais = st.text_area("Liste os ingredientes principais:")

tipo_culinaria = st.selectbox(
    "Qual é o tipo de culinária?",
    ["Brasileira", "Italiana", "Asiática", "Mexicana", "Qualquer uma"]
)

nivel_dificuldade = st.slider("Selecione o nível de dificuldade:", 1, 5, 3)
descricoes_dificuldade = {
    1: "Muito Fácil",
    2: "Fácil",
    3: "Intermediário",
    4: "Díficil",
    5: "Desafiador"
}
st.write(f"O nível de dificuldade escolhido foi: Nível {nivel_dificuldade} - {descricoes_dificuldade[nivel_dificuldade]}")

restricao_alimentar = st.checkbox("Você possui alguma restrição alimentar?")
if restricao_alimentar:
    restricao_resposta = st.text_input("Qual é o tipo da restrição alimentar?")
    if restricao_resposta:
        st.write(f"Sua restrição alimentar é: {restricao_resposta}")
else:
    st.write("Você não possui restrição alimentar.")

if st.button("Sugerir Receita"):
    if not ingredientes_principais:
        st.warning("Por favor, informe os ingredientes principais.")
    elif not tipo_culinaria:
        st.warning("Por favor, informe o tipo de culinária.")
    else:
        prompt_aluno = (
            f"Sugira uma receita'{tipo_culinaria}'.\n"
            f"Com nível de dificuldade {nivel_dificuldade}.\n"
            f"Deve usar principalmente os seguintes ingredientes: {ingredientes_principais}.\n"
            f"Apresente o nome da receita, uma lista de ingredientes adicionais se necessário, e um breve passo a passo."
        )

        if restricao_alimentar and restricao_resposta:
            prompt_aluno += f"A receita precisa ser adequada para a seguinte restrição alimenta: {restricao_resposta}.\n"

        st.markdown("---")
        st.markdown("⚙️ **Prompt que será enviado para a IA (para fins de aprendizado):**")
        st.text_area("",prompt_aluno, height=250)
        st.markdown("---")

        st.info("Aguarde, a IA está escolhendo a receita...")
        resposta_ia = gerar_resposta_gemini(prompt_aluno)

        if resposta_ia:
            st.markdown("### ✨ Sugestão de Receita da IA:")
            st.markdown(resposta_ia)
        else:
            st.error("Não foi possível gerar a receita. Verifique as mensagens acima ou tente novamente mais tarde.")