export default {
	async buscarCandidatosAlterar(cpf) {
		const codigoDigitado = cpf.replace(/\D/g, "").trim(); // remover tudo que não for numero
		
		console.log(codigoDigitado);
		if (!codigoDigitado || codigoDigitado.length !== 11) {
			showAlert('Por favor, digite um CPF com exatamente 11 dígitos.', 'info');
			return;
		}

		storeValue("buscaCandidatobyCPF", codigoDigitado);
		await fetchCandidatosByCPF.run();

		if (fetchCandidatosByCPF.data) {
			
			const candidatoData = fetchCandidatosByCPF.data;
			
			// Text3Copy.setText("Atualizando os dados de " + fetchCandidatosByCPF.data.nome + " com CPF " + fetchCandidatosByCPF.data.cpf);
			EntradaNomeAtualizar.setValue(candidatoData.nome);
			EntradaAniversarioAtualizar.setValue(candidatoData.data_nascimento)
			EntradaProfissoesAtualizar.setSelectedOptions(candidatoData.profissoes);
			showModal(ModalAtualizarCandidatos2.name);
			
			storeValue("cpfCandidatoAlterar", codigoDigitado);
			
		} else {
			showAlert('Concurso com o código ' + codigoDigitado + ' não encontrado.', 'warning');
		}
	}
}