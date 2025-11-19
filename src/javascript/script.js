// ============================================================
// Mostrar/esconder FELV e PORTE automaticamente
// ============================================================
document.getElementById("tipo_pet").addEventListener("change", () => {
    const tipo = document.getElementById("tipo_pet").value;

    document.getElementById("felv-box").style.display =
        tipo === "gato" ? "block" : "none";

    document.getElementById("porte-box").style.display =
        tipo === "cachorro" ? "block" : "none";
});


// ============================================================
// Coletar filtros do HTML
// ============================================================
function coletarFiltros() {
    const filtros = {};

    const tipo_pet = document.getElementById("tipo_pet").value;

    // cores (até 3)
    const selecionadas = [...document.querySelectorAll(".cor-checkbox:checked")]
        .map(i => i.value.toLowerCase());

    if (selecionadas.length > 0) filtros.cores = selecionadas;

    const sexo = document.getElementById("sexo").value;
    if (sexo !== "") filtros.sexo = parseInt(sexo);

    const idade = document.getElementById("idade").value;
    if (idade !== "") filtros.faixa_etaria = idade;

    const vac = document.getElementById("vacinado").value;
    if (vac !== "") filtros.vacinado = vac === "true";

    const soc = document.getElementById("sociavel").value;
    if (soc !== "") filtros.sociavel = soc === "true";

    const ani = document.getElementById("animado").value;
    if (ani !== "") filtros.animado = ani === "true";

    const cas = document.getElementById("castrado").value;
    if (cas !== "") filtros.castrado = cas === "true";

    const esp = document.getElementById("especial").value;
    if (esp !== "") filtros.adocao_especial = esp === "1";

    if (tipo_pet === "gato") {
        const felv = document.getElementById("felv").value;
        if (felv !== "") filtros.felv = parseInt(felv);
    }

    if (tipo_pet === "cachorro") {
        const porte = document.getElementById("porte").value;
        if (porte !== "") filtros.porte = parseInt(porte);
    }

    return { tipo_pet, filtros };
}



// ============================================================
// Enviar filtros ao backend (AGORA INCLUINDO df_talvez)
// ============================================================
document.getElementById("btn-buscar").addEventListener("click", async () => {
    const { tipo_pet, filtros } = coletarFiltros();

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
    }
});



// ============================================================
// Exibir lista de animais (3 por linha, centralizado, sem score)
// ============================================================
function exibirAnimais(lista, containerId) {
    const div = document.getElementById(containerId);
    div.innerHTML = "";

    if (!lista || lista.length === 0) {
        div.innerHTML = "<p>Nenhum pet encontrado.</p>";
        return;
    }

    div.style.display = "grid";
    div.style.gridTemplateColumns = "repeat(3, 1fr)";
    div.style.gap = "20px";
    div.style.justifyItems = "center";

    lista.forEach(pet => {
        const card = document.createElement("div");
        card.className = "animal-card";

        const img = document.createElement("img");
        img.src = `src/images/${pet.id}.png`;
        img.onerror = () => { img.src = "src/images/milu.png"; };
        img.className = "animal-img";

        const nome = document.createElement("h3");
        nome.innerText = pet.nome;
        nome.className = "animal-title";

        card.addEventListener("click", () => abrirPopup(pet));

        card.appendChild(img);
        card.appendChild(nome);
        div.appendChild(card);
    });
}



// ============================================================
// POPUP Modal
// ============================================================
function abrirPopup(pet) {
    document.getElementById("modal-img").innerHTML =
        `<img src="src/images/${pet.id}.png" class="animal-img" 
              onerror="this.src='src/images/milu.png'">`;

    let texto = `
        <strong>Nome:</strong> ${pet.nome || "-"}<br><br>
        <strong>Sexo:</strong> ${pet.sexo === 0 ? "Macho" : "Fêmea"}<br>
        <strong>Idade:</strong> ${pet.faixa_etaria || "-"}<br>
    `;

    if (pet.porte !== undefined && pet.porte !== null) {
        const mapPorte = {0: "Pequeno", 1: "Médio", 2: "Grande"};
        texto += `<strong>Porte:</strong> ${mapPorte[pet.porte] || "-"}<br>`;
    }

    if (pet.felv !== undefined && pet.felv !== null) {
        const mapFelv = {0: "Negativo", 1: "Positivo"};
        texto += `<strong>FELV:</strong> ${mapFelv[pet.felv] || "-"}<br>`;
    }

    if (pet.cores) {
        let cores = pet.cores;
        try {
            if (typeof cores === "string") {
                cores = JSON.parse(cores.replace(/'/g, '"'));
            }
        } catch {}
        if (Array.isArray(cores)) texto += `<strong>Cores:</strong> ${cores.join(", ")}<br>`;
    }

    const boolFields = [
        ["vacinado", "Vacinado"],
        ["sociavel", "Sociável"],
        ["animado", "Animado"],
        ["castrado", "Castrado"],
        ["adocao_especial", "Adoção especial"]
    ];

    boolFields.forEach(([campo, label]) => {
        if (pet[campo] !== undefined && pet[campo] !== null) {
            texto += `<strong>${label}:</strong> ${pet[campo] ? "Sim" : "Não"}<br>`;
        }
    });

    document.getElementById("modal-text").innerHTML = texto;
    document.getElementById("modal-info").style.display = "flex";
}

document.getElementById("fechar-modal").addEventListener("click", () => {
    document.getElementById("modal-info").style.display = "none";
});
