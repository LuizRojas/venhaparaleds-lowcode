export default {
	async buscarConcursoByCPF (cpf) {
		const cpf_limpo = cpf.replace(/\D/g, "").trim();  // deixar só numeros
		
		if (!cpf_limpo) {
			showAlert("Campo vazio. Por favor digite um valor!", "info");
			return;
		} else if (cpf_limpo.length !== 11) {
			showAlert("Formato incorreto. Por favor digite um valor válido.", "info");
			return;
		}
		
		try {
			storeValue("cpfCandidatoConcursoBuscar", cpf_limpo);
			
			const resposta = await getConcursosByCpf_Neon.run();
			
			if (!resposta || Object.keys(resposta).length === 0) {
        showAlert("Nenhum concurso encontrado para este candidato.", "warning");
        TabelaConcursos.setData([]);
        return;
      }

      TabelaConcursos.setData(resposta);
		} catch (e) {
			showAlert("Ocorreu um erro ao buscar candidatos pelo código " + cpf_limpo, "error");
      TabelaConcursos.setData([]);
		}
	}
}