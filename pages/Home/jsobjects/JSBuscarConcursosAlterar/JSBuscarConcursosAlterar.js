export default {
	async buscarConcursosAlterar(codigo) {
		const codigoDigitado = codigo.replace(/\D/g, "").trim(); // remover tudo que não for numero

		if (!codigoDigitado || codigoDigitado.length !== 11) {
			showAlert('Por favor, digite um CPF com exatamente 11 dígitos.', 'info');
			return;
		}

		storeValue("buscaConcursobyCodigo", codigoDigitado);
		await fetchConcursosByCodigoConcurso.run();

		if (fetchConcursosByCodigoConcurso.data) {
			
			const concursoData = fetchConcursosByCodigoConcurso.data;
			const [edicao, ano] = concursoData.edital.split("/");
			
			EntradaOrgaoAtualizar.setValue(concursoData.orgao);
			EntradaEditalEdicaoAtualizar.setValue(edicao);
			EntradaEditalAnoAtualizar.setValue(ano);
			// EntradaCodigoAtualizar.setValue(concursoData.codigo_concurso);
			EntradaVagasAtualizar.setSelectedOptions(concursoData.lista_vagas);
			showModal(ModalAtualizarConcursos2.name);
			
			storeValue("codigoConcursoAlterar", codigo);
			
		} else {
			showAlert('Concurso com o código ' + codigoDigitado + ' não encontrado.', 'warning');
		}
	}
}