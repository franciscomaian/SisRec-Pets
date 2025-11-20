// ============================================================
// Botão Editar
// ============================================================
document.getElementById("btn-edit").addEventListener("click", async () => {
    id_pet = document.getElementById("id_pet").value

    if (!id_pet) {
        alert("Digite um ID válido");
        return;
    }

    document.getElementById("edit-pet").style.display = "grid";
    document.getElementById("btn-att").textContent  = "Atualizar";

    const url = `http://127.0.0.1:8000/get/${id_pet}`;

    try {
        const resposta = await fetch(url, {
            method: "GET",
            headers: {"Content-Type": "application/json"}
        });

        if (!resposta.ok) throw new Error("Erro no servidor");

        const dados = await resposta.json();

        // --- COLOCAR NA CAIXAS OS VALORES ---
        document.getElementById("sexo").value = dados[0].sexo;
        document.getElementById("vacinado").value = dados[0].vacinado;
        document.getElementById("sociavel").value = dados[0].sociavel;
        document.getElementById("animado").value = dados[0].animado;
        document.getElementById("castrado").value = dados[0].castrado;
        document.getElementById("especial").value = dados[0].adocao_especial;

        if (dados[0].idade < 12) {
            document.getElementById("idade").value= "filhote";
        } else {
            document.getElementById("idade").value= "adulto";
        }

        //Falta marcar as cores
        

    } catch (e) {
        console.error(e);
        alert("Erro ao comunicar com o servidor");
    }
});


// ============================================================
// Botão Adicionar
// ============================================================
document.getElementById("btn-add").addEventListener("click", async () => {
    document.getElementById("edit-pet").style.display = "grid";
    document.getElementById("btn-att").textContent  = "Criar";
    /*const { tipo_pet, filtros } = coletarFiltros();

    if (!tipo_pet) {
        alert("Selecione Gato ou Cachorro");
        return;
    }

    const url = `http://127.0.0.1:8000/recomendar/${tipo_pet === "gato" ? "cat" : "dog"}`;

    try {
        const resposta = await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(filtros)
        });

        if (!resposta.ok) throw new Error("Erro no servidor");

        const dados = await resposta.json();

        // --- EXIBIR PRINCIPAIS ---
        exibirAnimais(dados.principais, "resultados");

        // --- EXIBIR TALVEZ VOCÊ GOSTE ---
        const contTalvez = document.getElementById("talvez-container");
        const divTalvez = document.getElementById("resultados-talvez");

        if (dados.talvez && dados.talvez.length > 0) {
            contTalvez.style.display = "block";
            exibirAnimais(dados.talvez, "resultados-talvez");
        } else {
            contTalvez.style.display = "none";
            divTalvez.innerHTML = "";
        }

    } catch (e) {
        console.error(e);
        alert("Erro ao comunicar com o servidor");
    }*/
});

// ============================================================
// Botão Remover
// ============================================================
document.getElementById("btn-remove").addEventListener("click", async () => {
    document.getElementById("edit-pet").style.display = "none";
    /*const { tipo_pet, filtros } = coletarFiltros();

    if (!tipo_pet) {
        alert("Selecione Gato ou Cachorro");
        return;
    }

    const url = `http://127.0.0.1:8000/recomendar/${tipo_pet === "gato" ? "cat" : "dog"}`;

    try {
        const resposta = await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(filtros)
        });

        if (!resposta.ok) throw new Error("Erro no servidor");

        const dados = await resposta.json();

        // --- EXIBIR PRINCIPAIS ---
        exibirAnimais(dados.principais, "resultados");

        // --- EXIBIR TALVEZ VOCÊ GOSTE ---
        const contTalvez = document.getElementById("talvez-container");
        const divTalvez = document.getElementById("resultados-talvez");

        if (dados.talvez && dados.talvez.length > 0) {
            contTalvez.style.display = "block";
            exibirAnimais(dados.talvez, "resultados-talvez");
        } else {
            contTalvez.style.display = "none";
            divTalvez.innerHTML = "";
        }

    } catch (e) {
        console.error(e);
        alert("Erro ao comunicar com o servidor");
    }*/
});