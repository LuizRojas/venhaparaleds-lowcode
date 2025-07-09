export default {
	async cadastrarConcurso() {
		const orgao = EntradaOrgaoInserir.text?.toUpperCase().trim();
		if (!orgao) {
			showAlert("Preencha o campo 'Órgão'.", "info");
			return;
		}

		const edital_edicao = EntradaEditalEdicaoInserir.text.replace(/\D/g, "").trim();
		if (!edital_edicao) {
			showAlert("Preencha o campo 'Edição edital'.", "info");
			return;
		}

		const edital_ano = EntradaEditalAnoInserir.text.replace(/\D/g, "").trim();
		if (!edital_ano) {
			showAlert("Preencha o campo 'Ano edital'.", "info");
			return;
		}

		const edital_formatado = `${edital_edicao}/${edital_ano}`;
		storeValue("editalFormatadoInserir", edital_formatado);

		const codigo_concurso = EntradaCodigoConcursoInserir.text?.trim();
		if (!codigo_concurso) {
			showAlert("Preencha o campo 'Código do Concurso'.", "info");
			return;
		}

		const lista_vagas = ListaVagasInserir.selectedOptionValues;
		if (!lista_vagas || lista_vagas.length === 0) {
			showAlert("Selecione pelo menos uma vaga!", "info");
			return;
		}

		try {
			await addConcursoAPI.run();
			showAlert("Concurso cadastrado com sucesso!", "success");
			EntradaOrgaoInserir.setValue("");
			EntradaEditalEdicaoInserir.setValue("");
			EntradaEditalAnoInserir.setValue("");
			EntradaCodigoConcursoInserir.setValue("");
			ListaVagasInserir.setSelectedOptions([]);
		} catch (error) {
			console.log("Erro ao cadastrar concurso:", error);
			if (error?.message?.includes("409")) {
				showAlert("Esse concurso já está cadastrado.", "warning");
			} else {
				showAlert("Erro ao cadastrar o concurso. Tente novamente.", "error");
			}
		}
	}
};
