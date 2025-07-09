export default {
	async buscarCandidatosByCodigo(codigo) {
		const codigo_limpo = codigo.replace(/\D/g, "").trim();  // remove tudo que não é número

		if (!codigo_limpo) {
			showAlert("Campo vazio. Por favor, digite um valor!", "info");
			return; // precisa retornar aqui
		} else if (codigo_limpo.length !== 11) {
			showAlert("O código deve ter 11 dígitos.", "info");
			return; // precisa retornar aqui também
		}

		try {
			storeValue("codigoConcursoCandidatoBuscar", codigo_limpo);

			const resposta = await fetchCandidatosDataByCodigo.run();

			if (!resposta || Object.keys(resposta).length === 0) {
				showAlert("Nenhum candidato encontrado para este código.", "warning");
				TabelaCandidatos.setData([]);
				return;
			}

			TabelaCandidatos.setData(resposta);
		} catch (e) {
			showAlert("Ocorreu um erro ao buscar candidatos pelo código " + codigo_limpo, "error");
			TabelaCandidatos.setData([]);
		}
	}
}