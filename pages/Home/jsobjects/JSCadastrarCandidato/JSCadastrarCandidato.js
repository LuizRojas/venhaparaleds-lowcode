export default {
	async cadastrarCandidato() {
		const nome = EntradaNomeInserir.text.trim();
		if (!nome) {
			showAlert("Preencha o campo 'Nome'.", "info");
			return;
		}

		if (/\d/.test(nome)) {
			showAlert("O campo 'Nome' não pode conter números!.", "info");
			return;
		}
		const aniversario = EntradaAniversarioInserir.formattedDate;
		if (!aniversario) {
			showAlert("Preencha o campo 'Aniversário'.", "info");
			return;
		}

		const cpf = EntradaCPFInserir.text.replace(/\D/g, "").trim();
		if (!cpf) {
			showAlert("Preencha o campo 'CPF'.", "info");
			return;
		} else if (cpf.length !== 11) {
			showAlert("Digite o CPF corretamente.", "info");
			return;
		}

		const profissoes = ProfissoesInserir.selectedOptionValues;
		if (!profissoes || profissoes.length === 0) {
			showAlert("Selecione pelo menos uma profissão!", "info");
			return;
		}

		// storeValue("nomeCandidatoInserir", nome);
		// storeValue("aniversarioCandidatoInserir", aniversario);
		// storeValue("cpfCandidatoInserir", cpf);
		// storeValue("profissoesCandidatoInserir", profissoes)

		try {
			await addCandidato_Neon.run();
			showAlert("Candidato cadastrado com sucesso!", "success");
			EntradaNomeInserir.setValue("");
			EntradaCPFInserir.setValue("");
			EntradaAniversarioInserir.setValue("");
			ProfissoesInserir.setSelectedOptions([]);
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
