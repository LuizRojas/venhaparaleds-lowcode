export default {
	limparCampos() {
		EntradaDeletarCandidatosBusca.setValue("");
		TabelaInformacoesCandidatosDel.setData([]);
		BotaoDeletarCandidato.setDisabled(true);
		// removeValue("valorBuscaDeletarCandidato");
		// removeValue("buscaCandidatobyCodigo");
	},
	
	async confirmarDeletarCandidato () {
		try {
			await deleteCandidatoAPI.run();
			showAlert(
				"Candidato com CPF " + appsmith.store.buscaCandidatoByCPF + " foi deletado com sucesso!",
				"info"
			);
			showModal(ModalDeletarCandidatos.name);
		}	catch (e) {
			showAlert("Erro ao deletar o candidato!", "error");
			console.log("Erro ao deletar: ", e);
		}
	}
}