export default {
	async buscarCandidatosAlterar(cpf) {
		const cpfDigitado = cpf.replace(/\D/g, "").trim(); // Remover tudo que não for numero
		
		console.log("DEBUG: CPF digitado (limpo):", cpfDigitado); // Log para depuração

		if (!cpfDigitado || cpfDigitado.length !== 11) {
			showAlert('Por favor, digite um CPF com exatamente 11 dígitos.', 'info');
			return;
		}

		storeValue("buscaCandidatobyCPF", cpfDigitado);
		// CORREÇÃO: Executa a query e o dado estará em getCandidatoByCPF_Neon.data
		await getCandidatoByCPF_Neon.run({
            variables: { // Passa o CPF como variável para a query
                cpfCandidatoParam: cpfDigitado
            }
        });
		
		// CORREÇÃO: Verifica se a query retornou dados E se o array não está vazio
		if (getCandidatoByCPF_Neon.data && getCandidatoByCPF_Neon.data.length > 0) {
			// CORREÇÃO: Acessa o PRIMEIRO (e único) elemento do array de dados retornado pela query
			const candidatoData = getCandidatoByCPF_Neon.data[0];
			
			console.log("DEBUG: Dados do candidato encontrados:", candidatoData); // Log para depuração

			// Preenche os campos do modal de atualização com os dados do candidato
			EntradaNomeAtualizar.setValue(candidatoData.nome);
			// CORREÇÃO: O DatePicker espera a data no formato YYYY-MM-DD para setValue
			// Sua API retorna no formato DD/MM/YYYY, então precisa converter.
			// moment(string, "DD/MM/YYYY").format("YYYY-MM-DD")
			EntradaAniversarioAtualizar.setValue(candidatoData.data_nascimento);
			
			// CORREÇÃO: Usar setValue() para o MultiSelect
			EntradaProfissoesAtualizar.setSelectedOptions(candidatoData.profissoes);
			
			showModal(ModalAtualizarCandidatos2.name);
			
			storeValue("cpfCandidatoAlterar", cpfDigitado);
			
		} else {
			// Se a query não retornou dados (candidato não encontrado)
			showAlert('Candidato com o CPF ' + cpfDigitado + ' não encontrado.', 'warning');
		}
	}
}
