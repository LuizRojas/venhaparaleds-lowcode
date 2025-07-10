export default {
	async buscarConcursosAlterar(codigo) {
		const codigoDigitado = codigo.replace(/\D/g, "").trim(); // remover tudo que não for numero

		if (!codigoDigitado || codigoDigitado.length !== 11) {
			showAlert('Por favor, digite um codigo com exatamente 11 dígitos.', 'info'); // Alerta menciona CPF, mas o contexto é código de concurso. Considere ajustar a mensagem.
			return;
		}

		storeValue("buscaConcursobyCodigo", codigoDigitado);
		await getConcursoCodigo_Neon.run();

		if (getConcursoCodigo_Neon.data && getConcursoCodigo_Neon.data.length > 0) { 
			
			const concursoData = getConcursoCodigo_Neon.data;
			
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
	},

    // A função atualizarConcurso que você forneceu para validação
    async atualizarConcurso () {
        const orgao  = EntradaOrgaoAtualizar.text.toUpperCase().trim();
        const edicao = EntradaEditalEdicaoAtualizar.text.replace(/\D/g, "").trim();
        const ano    = EntradaEditalAnoAtualizar.text.replace(/\D/g, "").trim();
        const vagas  = EntradaVagasAtualizar.selectedOptionValues;
				
			
        if (!orgao) {
            showAlert("Preencha o campo 'Órgão.'", "info");
            return;
        } else if (/\d/.test(orgao)) {
					showAlert("O campo 'Órgão' só pode ter letras!", "info");
					return;
				}
        if (!edicao) {
            showAlert("Preencha o campo 'Edição'.", "info");
            return;
        }
				
				if (!/^\d+$/.test(edicao.trim())) {  // se nao for composta por apenas digitos
					showAlert("O campo 'Edição' só pode ter números!", "info");
				}
        
        const currentYear = new Date().getFullYear();
        const minYear = 1900;
        const maxYear = currentYear + 10;

        if (!ano || !/^\d{4}$/.test(ano) || parseInt(ano) < minYear || parseInt(ano) > maxYear) {
            showAlert(`O campo 'Ano' deve ser um número de 4 dígitos entre ${minYear} e ${maxYear}.`, "info");
            return;
        }

        if (!vagas || vagas.length === 0) {
            showAlert("Preencha o campo 'Vagas'.", "info");
            return;
        }

        // const edital = edicao + "/" + ano;

        // salva os valores
        // storeValue("orgaoConcursoAlterar", orgao);
        // storeValue("editalFormatadoAlterar", edital);
        // storeValue("vagasConcursoAlterar", vagas);

        // try {
        await updateConcurso_Neon.run();
			
        if (updateConcurso_Neon.data) {
            showAlert("Concurso "+ EntradaCodigoConcursoInserir.text +" atualizado com sucesso", "success");
        } else {
            showAlert("Erro ao atualizar concurso.", "error");
            console.error("Erro: ao atualizar o concurso");
        }
        // } catch (e) {
        // showAlert("Erro inesperado ao atualizar concurso!", "error");
        // console.error("Exceção:", e);
        // }
    }
}
