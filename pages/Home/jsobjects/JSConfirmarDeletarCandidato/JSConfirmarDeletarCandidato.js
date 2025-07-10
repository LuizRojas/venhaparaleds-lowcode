export default {
	limparCampos() {
		EntradaDeletarCandidatosBusca.setValue("");
		TabelaInformacoesCandidatosDel.setData([]);
		BotaoDeletarCandidato.setDisabled(true);
		// removeValue("valorBuscaDeletarCandidato");
		// removeValue("buscaCandidatobyCodigo");
	},
	
	async confirmarDeletarCandidato () {
		await deleteCandidato_Neon.run();
		if (deleteCandidato_Neon.data){
			showAlert(
				"Candidato com CPF " + appsmith.store.buscaCandidatoByCPF + " foi deletado com sucesso!",
				"info"
			);
		} else {
				showModal(ModalDeletarCandidatos.name);
				showAlert("Erro ao deletar o candidato!", "error");
				console.log("Erro ao deletar: ", e);
			}
		}
}