export default {
	async atualizarCandidato () {
		const nome  = EntradaNomeAtualizar.text.trim();
		const aniversario = EntradaAniversarioAtualizar.formattedDate;
		const profissoes  = EntradaProfissoesAtualizar.selectedOptionValues;

		if (!nome) {
			showAlert("Preencha o campo 'Nome'.", "info");
			return;
		}
		if (!aniversario) {
			showAlert("Preencha o campo 'Aniversário'.", "info");
			return;
		}
		if (!profissoes || profissoes.length === 0) {
			showAlert("Preencha o campo 'Profissões'.", "info");
			return;
		}

		// salva os valores
		storeValue("nomeCandidatoAlterar", nome);
		storeValue("AniversarioCandidatoAlterar", aniversario);
		storeValue("profissoesCandidatoAlterar", profissoes);

		const resposta = await updateCandidatoAPI.run();
		const statusCodeRaw = updateCandidatoAPI.responseMeta?.statusCode || "";
		const statusCode = parseInt(statusCodeRaw);

		if (statusCode >= 200 && statusCode < 300) {
			showAlert("Candidato atualizado com sucesso", "success");
		} else {
			showAlert("Erro ao atualizar Candidato. Código: " + statusCode, "error");
			console.error("Erro:", resposta);
		}
}
}