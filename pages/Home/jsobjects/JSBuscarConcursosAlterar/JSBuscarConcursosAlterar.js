export default {
	async buscarConcursosAlterar(codigo) {
		const codigoDigitado = codigo.replace(/\D/g, "").trim(); // remover tudo que não for numero

		if (!codigoDigitado || codigoDigitado.length !== 11) {
			showAlert('Por favor, digite um CPF com exatamente 11 dígitos.', 'info'); // Alerta menciona CPF, mas o contexto é código de concurso. Considere ajustar a mensagem.
			return;
		}

		storeValue("buscaConcursobyCodigo", codigoDigitado);
		await getConcursoCodigo_Neon.run();

		// CORREÇÃO AQUI: Verifica se a query retornou dados E se o array não está vazio
		if (getConcursoCodigo_Neon.data && getConcursoCodigo_Neon.data.length > 0) { 
			
			const concursoData = getConcursoCodigo_Neon.data[0]; // CORREÇÃO: Acessa o PRIMEIRO elemento do array de dados
			
			// Agora, concursoData deve ser o objeto do concurso, e .edital deve existir
			const [edicao, ano] = concursoData.edital.split("/"); 
			
			EntradaOrgaoAtualizar.setValue(concursoData.orgao);
			EntradaEditalEdicaoAtualizar.setValue(edicao);
			EntradaEditalAnoAtualizar.setValue(ano);
			// EntradaCodigoAtualizar.setValue(concursoData.codigo_concurso); // Linha comentada
			
			// CORREÇÃO AQUI: Usar setValue() para o MultiSelect
			EntradaVagasAtualizar.setSelectedOptions(concursoData.lista_vagas); 
			
			showModal(ModalAtualizarConcursos2.name);
			
			storeValue("codigoConcursoAlterar", codigo);
			
		} else {
			showAlert('Concurso com o código ' + codigoDigitado + ' não encontrado.', 'warning');
		}
	}
}
