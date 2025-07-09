export default {
	async atualizarConcurso () {
		const orgao  = EntradaOrgaoAtualizar.text.toUpperCase().trim();
		const edicao = EntradaEditalEdicaoAtualizar.text.replace(/\D/g, "").trim();
		const ano    = EntradaEditalAnoAtualizar.text.replace(/\D/g, "").trim();
		const vagas  = EntradaVagasAtualizar.selectedOptionValues;
		
		if (!orgao) {
			showAlert("Preencha o campo 'Órgão.'", "info");
			return;
		}
		if (!edicao) {
			showAlert("Preencha o campo 'Edição'.", "info");
			return;
		}
		if (!ano) {
			showAlert("Preencha o campo 'Ano'.", "info");
			return;
		}
		if (!vagas || vagas.length === 0) {
			showAlert("Preencha o campo 'Vagas'.", "info");
			return;
		}
		
		const edital = edicao + "/" + ano;

		// salva os valores
		storeValue("orgaoConcursoAlterar", orgao);
		storeValue("editalFormatadoAlterar", edital);
		storeValue("vagasConcursoAlterar", vagas);

		// try {
			const resposta = await updateConcursoAPI.run();
			const statusCodeRaw = updateConcursoAPI.responseMeta?.statusCode || "";
			const statusCode = parseInt(statusCodeRaw);

			if (statusCode >= 200 && statusCode < 300) {
				showAlert("Concurso atualizado com sucesso", "success");
			} else {
				showAlert("Erro ao atualizar concurso. Código: " + statusCode, "error");
				console.error("Erro:", resposta);
			}
		// } catch (e) {
			// showAlert("Erro inesperado ao atualizar concurso!", "error");
			// console.error("Exceção:", e);
		// }
	}
}
