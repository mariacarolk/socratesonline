// Estados e cidades do Brasil
const cidadesPorEstado = {
  'AC': ['Rio Branco', 'Cruzeiro do Sul', 'Sena Madureira', 'Tarauacá', 'Feijó', 'Senador Guiomard', 'Plácido de Castro', 'Brasiléia', 'Xapuri', 'Epitaciolândia'],
  'AL': ['Maceió', 'Arapiraca', 'Palmeira dos Índios', 'Rio Largo', 'Penedo', 'União dos Palmares', 'São Miguel dos Campos', 'Santana do Ipanema', 'Delmiro Gouveia', 'Coruripe'],
  'AP': ['Macapá', 'Santana', 'Laranjal do Jari', 'Oiapoque', 'Mazagão', 'Porto Grande', 'Tartarugalzinho', 'Vitória do Jari', 'Ferreira Gomes', 'Pedra Branca do Amapari'],
  'AM': ['Manaus', 'Parintins', 'Itacoatiara', 'Manacapuru', 'Coari', 'Tefé', 'Tabatinga', 'Maués', 'São Gabriel da Cachoeira', 'Humaitá'],
  'BA': ['Salvador', 'Feira de Santana', 'Vitória da Conquista', 'Camaçari', 'Juazeiro', 'Ilhéus', 'Itabuna', 'Lauro de Freitas', 'Jequié', 'Teixeira de Freitas', 'Alagoinhas', 'Barreiras', 'Simões Filho', 'Paulo Afonso', 'Eunápolis', 'Porto Seguro'],
  'CE': ['Fortaleza', 'Caucaia', 'Juazeiro do Norte', 'Maracanaú', 'Sobral', 'Crato', 'Itapipoca', 'Maranguape', 'Iguatu', 'Quixadá', 'Canindé', 'Aquiraz', 'Pacatuba', 'Crateús', 'Russas'],
  'DF': ['Brasília', 'Gama', 'Taguatinga', 'Ceilândia', 'Sobradinho', 'Planaltina', 'Samambaia', 'Santa Maria', 'São Sebastião', 'Recanto das Emas'],
  'ES': ['Vitória', 'Cariacica', 'Serra', 'Vila Velha', 'Linhares', 'Colatina', 'Guarapari', 'São Mateus', 'Cachoeiro de Itapemirim', 'Aracruz', 'Viana', 'Nova Venécia', 'Barra de São Francisco'],
  'GO': ['Goiânia', 'Aparecida de Goiânia', 'Anápolis', 'Rio Verde', 'Luziânia', 'Águas Lindas de Goiás', 'Valparaíso de Goiás', 'Trindade', 'Formosa', 'Novo Gama', 'Itumbiara', 'Senador Canedo', 'Catalão', 'Jataí', 'Planaltina'],
  'MA': ['São Luís', 'Imperatriz', 'São José de Ribamar', 'Timon', 'Caxias', 'Codó', 'Paço do Lumiar', 'Açailândia', 'Bacabal', 'Balsas', 'Barra do Corda', 'Santa Inês', 'Pinheiro', 'Pedreiras'],
  'MT': ['Cuiabá', 'Várzea Grande', 'Rondonópolis', 'Sinop', 'Tangará da Serra', 'Cáceres', 'Sorriso', 'Lucas do Rio Verde', 'Barra do Garças', 'Primavera do Leste', 'Alta Floresta', 'Ponta Porã'],
  'MS': ['Campo Grande', 'Dourados', 'Três Lagoas', 'Corumbá', 'Ponta Porã', 'Naviraí', 'Nova Andradina', 'Sidrolândia', 'Maracaju', 'São Gabriel do Oeste', 'Coxim', 'Aquidauana'],
  'MG': ['Belo Horizonte', 'Uberlândia', 'Contagem', 'Juiz de Fora', 'Betim', 'Montes Claros', 'Ribeirão das Neves', 'Uberaba', 'Governador Valadares', 'Ipatinga', 'Sete Lagoas', 'Divinópolis', 'Santa Luzia', 'Ibirité', 'Poços de Caldas', 'Patos de Minas', 'Pouso Alegre', 'Teófilo Otoni', 'Barbacena', 'Sabará', 'Vespasiano', 'Conselheiro Lafaiete', 'Varginha', 'Itabira', 'Passos'],
  'PA': ['Belém', 'Ananindeua', 'Santarém', 'Marabá', 'Parauapebas', 'Castanhal', 'Abaetetuba', 'Cametá', 'Marituba', 'Bragança', 'Altamira', 'Itaituba', 'Tucuruí', 'Benevides'],
  'PB': ['João Pessoa', 'Campina Grande', 'Santa Rita', 'Patos', 'Bayeux', 'Sousa', 'Cajazeiras', 'Cabedelo', 'Guarabira', 'Mamanguape', 'Sapé', 'Itabaiana', 'Monteiro', 'Pombal'],
  'PR': ['Curitiba', 'Londrina', 'Maringá', 'Ponta Grossa', 'Cascavel', 'São José dos Pinhais', 'Foz do Iguaçu', 'Colombo', 'Guarapuava', 'Paranaguá', 'Araucária', 'Toledo', 'Apucarana', 'Pinhais', 'Campo Largo', 'Arapongas', 'Almirante Tamandaré', 'Umuarama', 'Paranavaí', 'Sarandi'],
  'PE': ['Recife', 'Jaboatão dos Guararapes', 'Olinda', 'Caruaru', 'Petrolina', 'Paulista', 'Cabo de Santo Agostinho', 'Camaragibe', 'Garanhuns', 'Vitória de Santo Antão', 'Igarassu', 'São Lourenço da Mata', 'Santa Cruz do Capibaribe', 'Abreu e Lima', 'Ipojuca', 'Serra Talhada', 'Araripina', 'Gravatá', 'Carpina'],
  'PI': ['Teresina', 'Parnaíba', 'Picos', 'Piripiri', 'Floriano', 'Campo Maior', 'Barras', 'União', 'Altos', 'Pedro II', 'Valença do Piauí', 'Esperantina', 'São Raimundo Nonato', 'Cocal'],
  'RJ': ['Rio de Janeiro', 'São Gonçalo', 'Duque de Caxias', 'Nova Iguaçu', 'Niterói', 'Belford Roxo', 'São João de Meriti', 'Campos dos Goytacazes', 'Petrópolis', 'Volta Redonda', 'Magé', 'Macaé', 'Itaboraí', 'Cabo Frio', 'Angra dos Reis', 'Nova Friburgo', 'Barra Mansa', 'Teresópolis', 'Mesquita', 'Nilópolis'],
  'RN': ['Natal', 'Mossoró', 'Parnamirim', 'São Gonçalo do Amarante', 'Macaíba', 'Ceará-Mirim', 'Caicó', 'Assu', 'Currais Novos', 'Nova Cruz', 'São José de Mipibu', 'Apodi', 'João Câmara', 'Pau dos Ferros'],
  'RS': ['Porto Alegre', 'Caxias do Sul', 'Pelotas', 'Canoas', 'Santa Maria', 'Gravataí', 'Viamão', 'Novo Hamburgo', 'São Leopoldo', 'Rio Grande', 'Alvorada', 'Passo Fundo', 'Sapucaia do Sul', 'Uruguaiana', 'Santa Cruz do Sul', 'Cachoeirinha', 'Bagé', 'Bento Gonçalves', 'Erechim', 'Guaíba', 'Cachoeira do Sul'],
  'RO': ['Porto Velho', 'Ji-Paraná', 'Ariquemes', 'Vilhena', 'Cacoal', 'Rolim de Moura', 'Guajará-Mirim', 'Jaru', 'Ouro Preto do Oeste', 'Machadinho do Oeste'],
  'RR': ['Boa Vista', 'Rorainópolis', 'Caracaraí', 'Alto Alegre', 'Mucajaí', 'São Luiz', 'São João da Baliza', 'Pacaraima', 'Iracema', 'Amajari'],
  'SC': ['Florianópolis', 'Joinville', 'Blumenau', 'São José', 'Criciúma', 'Chapecó', 'Itajaí', 'Lages', 'Jaraguá do Sul', 'Palhoça', 'Balneário Camboriú', 'Brusque', 'Tubarão', 'São Bento do Sul', 'Caçador', 'Camboriú', 'Navegantes', 'Concórdia', 'Rio do Sul', 'Araranguá'],
  'SP': ['São Paulo', 'Guarulhos', 'Campinas', 'São Bernardo do Campo', 'Santo André', 'Osasco', 'Ribeirão Preto', 'Sorocaba', 'Mauá', 'São José dos Campos', 'Mogi das Cruzes', 'Diadema', 'Jundiaí', 'Carapicuíba', 'Piracicaba', 'Bauru', 'Itaquaquecetuba', 'São Vicente', 'Franca', 'Guarujá', 'Taubaté', 'Praia Grande', 'Limeira', 'Suzano', 'Taboão da Serra', 'Sumaré', 'Barueri', 'Embu das Artes', 'São Carlos', 'Marília'],
  'SE': ['Aracaju', 'Nossa Senhora do Socorro', 'Lagarto', 'Itabaiana', 'São Cristóvão', 'Estância', 'Tobias Barreto', 'Simão Dias', 'Propriá', 'Capela'],
  'TO': ['Palmas', 'Araguaína', 'Gurupi', 'Porto Nacional', 'Paraíso do Tocantins', 'Colinas do Tocantins', 'Guaraí', 'Tocantinópolis', 'Miracema do Tocantins', 'Dianópolis']
};

// Script para carregar cidades dinamicamente baseado no estado selecionado

// Inicializar autocompletar de cidades quando o documento carregar
document.addEventListener('DOMContentLoaded', function() {
  initCidadeEstadoForms();
});

// Função para inicializar todos os formulários com campos cidade/estado
function initCidadeEstadoForms() {
  // Buscar todos os selects de estado
  const estadoSelects = document.querySelectorAll('select[name="estado"], #estado');
  
  estadoSelects.forEach(estadoSelect => {
    // Encontrar o campo cidade correspondente
    const formContainer = estadoSelect.closest('form') || estadoSelect.closest('.form-container') || document;
    const cidadeInput = formContainer.querySelector('input[name="cidade"], #cidade');
    
    if (cidadeInput) {
      setupCidadeEstado(estadoSelect, cidadeInput);
    }
  });
}

// Função para configurar um par estado/cidade específico
function setupCidadeEstado(estadoSelect, cidadeInput) {
  // Criar datalist para autocompletar se não existir
  let datalist = document.getElementById(`cidades-list-${estadoSelect.id || 'default'}`);
  if (!datalist) {
    datalist = document.createElement('datalist');
    datalist.id = `cidades-list-${estadoSelect.id || 'default'}`;
    cidadeInput.setAttribute('list', datalist.id);
    document.body.appendChild(datalist);
  }
  
  // Event listener para mudança de estado
  estadoSelect.addEventListener('change', function() {
    const estadoSelecionado = this.value;
    
    // Limpar o campo cidade
    cidadeInput.value = '';
    
    // Limpar o datalist
    datalist.innerHTML = '';
    
    if (estadoSelecionado) {
      // Buscar cidades via API
      carregarCidades(estadoSelecionado, datalist, cidadeInput, estadoSelect);
    } else {
      cidadeInput.placeholder = 'Cidade';
      cidadeInput.disabled = true;
    }
  });
  
  // Se já há um estado selecionado, carregar as cidades
  if (estadoSelect.value) {
    carregarCidades(estadoSelect.value, datalist, cidadeInput, estadoSelect);
  } else {
    cidadeInput.disabled = true;
  }
}

// Função para carregar cidades via API
function carregarCidades(estado, datalist, cidadeInput, estadoSelect) {
  // Mostrar loading
  cidadeInput.placeholder = 'Carregando cidades...';
  cidadeInput.disabled = true;
  
  // Fazer requisição para a API
  fetch(`/api/cidades/${estado}`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Limpar e popular o datalist
        datalist.innerHTML = '';
        
        data.cidades.forEach(cidade => {
          const option = document.createElement('option');
          option.value = cidade;
          datalist.appendChild(option);
        });
        
        // Atualizar placeholder e habilitar campo
        const nomeEstado = estadoSelect.options[estadoSelect.selectedIndex].text;
        cidadeInput.placeholder = `Digite ou selecione uma cidade de ${nomeEstado}`;
        cidadeInput.disabled = false;
        
        console.log(`Carregadas ${data.cidades.length} cidades para ${estado}`);
      } else {
        console.error('Erro ao carregar cidades:', data.message);
        cidadeInput.placeholder = 'Erro ao carregar cidades';
        cidadeInput.disabled = false;
      }
    })
    .catch(error => {
      console.error('Erro na requisição:', error);
      cidadeInput.placeholder = 'Erro ao carregar cidades';
      cidadeInput.disabled = false;
    });
}

// Função para validar se a cidade está na lista (opcional)
function validarCidade(cidadeInput, estado) {
  if (!estado || !cidadeInput.value) {
    return true; // Validação passa se não há valores para validar
  }
  
  return fetch(`/api/cidades/${estado}`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const cidadeDigitada = cidadeInput.value.trim().toLowerCase();
        const cidadeEncontrada = data.cidades.some(cidade => 
          cidade.toLowerCase() === cidadeDigitada
        );
        
        if (!cidadeEncontrada) {
          console.warn(`Cidade "${cidadeInput.value}" não encontrada na lista de ${estado}`);
          // Opcionalmente, você pode mostrar um aviso ao usuário
          // ou forçar a seleção apenas de cidades válidas
        }
        
        return cidadeEncontrada;
      }
      return true; // Em caso de erro na API, deixa passar a validação
    })
    .catch(error => {
      console.error('Erro ao validar cidade:', error);
      return true; // Em caso de erro, deixa passar a validação
    });
} 