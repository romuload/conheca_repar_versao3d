// Conteúdo extraído de jogo_como_funciona.swf (2007).
// Respostas certas confirmadas jogando o SWF original (10/10 = 1000 pts).
// `correta` é o índice (0-based) da alternativa certa, na ordem em que aparecem no jogo.
// `cena` descreve a ilustração de fundo de cada etapa (rótulos das setas do fluxo).

const ETAPAS = [
  {
    etapa: 1,
    cena: { titulo: "Terminal São Francisco do Sul", rotulos: ["Petroleiro", "Monobóia", "Oleoduto", "Tanque de petróleo"] },
    pergunta: "De que terminal marítimo o petróleo extraído é transportado?",
    alternativas: ["São Francisco do Sul", "Florianópolis", "Todos os Santos"],
    correta: 0,
    explicacao:
      "O petróleo que é extraído dos poços marítimos é transportado por navios petroleiros até o terminal marítimo de São Francisco do Sul – onde se dá o escoamento, através da monobóia e dutos marinhos, até os tanques do Terminal. Atualmente, o elenco de petróleo recebido tem sua maior parte proveniente da Bacia de Campos, para o petróleo nacional, e da Nigéria, para petróleo importado. Aproximadamente 70% é nacional e 30%, importado."
  },
  {
    etapa: 2,
    cena: { titulo: "Unidade de Destilação", rotulos: ["GLP", "Nafta leve", "Nafta pesada", "Querosene", "Diesel", "RAT"] },
    pergunta: "A que temperatura o óleo bruto é aquecido quando sai do Tanque de Petróleo Repar?",
    alternativas: ["500º", "250º", "140º"],
    correta: 1,
    explicacao:
      "A primeira etapa do processo de refino é a destilação atmosférica. O petróleo é aquecido a temperatura de 250º e fracionado em uma torre que possui pratos perfurados em várias alturas. Como a parte inferior da torre é mais quente, os hidrocarbonetos gasosos sobem e se condensam ao passarem pelos pratos. Nessa etapa são extraídos, por ordem crescente de densidade, gases combustíveis, GLP, Gasolina, Nafta, Solventes, Querosenes, Óleo Diesel e um óleo pesado, chamado resíduo atmosférico (RAT), que é extraído do fundo da torre."
  },
  {
    etapa: 3,
    cena: { titulo: "Unidade a Vácuo", entrada: ["Resíduo atmosférico"], rotulos: ["Diesel pesado", "Gasóleo", "RV"] },
    pergunta: "Onde será processado o resíduo de vácuo escoado na parte inferior da torre?",
    alternativas: ["Craqueamento", "Destilação", "Desasfaltação"],
    correta: 2,
    explicacao:
      "O resíduo atmosférico é então reaquecido e levado para uma outra torre (Unidade a Vácuo), onde o seu fracionamento ocorrerá a uma pressão abaixo da atmosfera. Nessa torre será extraída mais uma parcela de Óleo Diesel e um produto chamado genericamente de Gasóleo, que não constitui um produto acabado, mas sim intermediário. O Gasóleo servirá como matéria-prima para produção de mais gases combustíveis, GLP, gasolina e outros, no Craqueamento.\n\nO resíduo de fundo da destilação a vácuo (chamado de RV, ou Resíduo de Vácuo) é escoado na parte inferior da torre e será processado na Desasfaltação."
  },
  {
    etapa: 4,
    cena: { titulo: "Unidade de Craqueamento", entrada: ["Gasóleo"], rotulos: ["GLP (2)", "Nafta craqueada", "Diluente para óleo combustível"] },
    pergunta: "Quais são as modalidades de Craqueamento existentes no processo de destilação?",
    alternativas: ["Destilação e Térmico", "Térmico e Catalítico", "Catalítico e Desasfaltação"],
    correta: 1,
    explicacao:
      "Este processo quebra as moléculas de hidrocarbonetos intermediários, convertendo-as em nafta, que irão compor a GASOLINA, e outros derivados de maior valor comercial. Os dois principais tipos são o craqueamento térmico e o catalítico. O térmico utiliza calor e altas pressões para efetuar a conversão de moléculas grandes em outras menores e o catalítico utiliza um catalisador, que é uma substância que facilita essa conversão, porém em condições de pressão mais reduzidas. Os catalisadores mais usados são: platina, alumina, bentanina ou sílica.\n\nNa Repar, o processo utilizado é o craqueamento catalítico. Desse processo, resultarão GLP, Nafta Craqueada e diluente para Óleo Combustível. Esse último será integrado ao Resíduo Asfáltico."
  },
  {
    etapa: 5,
    cena: { titulo: "GLP (gás de cozinha)", entrada: ["GLP (destilação)", "GLP (craqueamento)"], rotulos: ["Esfera", "Distribuidora"] },
    pergunta: "O GLP é popularmente conhecido como:",
    alternativas: ["Óleo Diesel", "Gás de Cozinha", "Asfalto"],
    correta: 1,
    explicacao:
      "O GLP proveniente dos processos de destilação e craqueamento fica armazenado em esferas. Conhecido popularmente como gás de cozinha, o GLP é obtido a partir das frações mais leves do petróleo. No caso da Repar, é a mistura de C3 (Propano) e C4 (Butano)."
  },
  {
    etapa: 6,
    cena: { titulo: "Unidade de Desasfaltação", entrada: ["Resíduo de vácuo", "Diluente para óleo combustível (craqueamento)"], rotulos: ["Resíduo asfáltico", "Matéria-prima", "Fosfértil"] },
    pergunta: "O resíduo de fundo da destilação a vácuo é processado na Unidade de Desasfaltação, dando origem ao:",
    alternativas: ["Óleo desasfaltado", "Óleo Diesel", "Querosene"],
    correta: 0,
    explicacao:
      "O RV segue para a Unidade de Desasfaltação, onde dará origem a Óleo Desasfaltado (ODES) e Resíduo Asfáltico (RASF). O ODES vai se juntar ao Gasóleo em tanque e o Resíduo Asfáltico vira: matéria-prima para a Fosfertil (fertilizantes e matérias-primas para indústrias químicas); óleo combustível, nas suas várias qualidades; ou cimento asfáltico pesado (CAP).\n\nO ASFALTO\nOriginalmente, o asfalto é encontrado dissolvido no petróleo e pode ser obtido por evaporação natural de depósitos localizados à superfície terrestre (asfalto natural) ou por processo em unidades industriais a partir do óleo combustível. Quimicamente é formado por uma mistura de hidrocarbonetos não voláteis de elevada massa molecular e pode ser encontrado sob a forma líquida, viscosa ou semi-sólida. O betume é o elemento ativo do asfalto e transfere a ele a propriedade impermeabilizante e aglutinante."
  },
  {
    etapa: 7,
    cena: { titulo: "Gasolina", entrada: ["Nafta leve (destilação)", "Nafta craqueada"], rotulos: ["Distribuidora", "Posto"] },
    pergunta: "A combinação de Nafta Leve e de Nafta Craqueada dá origem a:",
    alternativas: ["Óleo Diesel", "Gasolina B", "Gasolina A"],
    correta: 2,
    explicacao:
      "A gasolina A é resultante da combinação da nafta leve originária da destilação e da nafta craqueada, originária do craqueamento.\n\nA GASOLINA\nA gasolina é líquida, volátil, inflamável e constituída quimicamente por uma mistura complexa de mais de 400 hidrocarbonetos. As características e especificações dos componentes da gasolina são regulamentadas pela Agência Nacional de Petróleo (ANP). O octano é um dos hidrocarbonetos presentes em qualquer tipo de gasolina e sua importância está relacionada com uma das principais propriedades do combustível: o poder antidetonante, daí o termo “octanagem”."
  },
  {
    etapa: 8,
    cena: { titulo: "Diesel", entrada: ["Diesel pesado"], rotulos: ["Diesel leve", "Nafta pesada", "Querosene", "Mistura", "Diesel para uso em motores"] },
    pergunta: "O diesel comercializado é resultante do processo de:",
    alternativas: ["Hidrodessulfurização", "Octanagem", "Destilação"],
    correta: 0,
    explicacao:
      "O Diesel Pesado originário da destilação passa pelo processo de hidrodessulfurização (retirada de compostos de enxofre) e é combinado às Naftas Pesada e Leve, ao Querosene e ao Diesel Leve para resultar no diesel que será comercializado.\n\nO DIESEL\nO Diesel é constituído basicamente por hidrocarbonetos. Possui concentrações baixas de enxofre, nitrogênio e oxigênio. É um produto inflamável, medianamente tóxico, volátil, límpido, isento de material em suspensão e com odor forte e característico. O Óleo Diesel é utilizado em motores de combustão interna e ignição por compressão empregados nas mais diversas aplicações. Desde 1994, a Petrobras produz dois tipos de óleo diesel - o metropolitano e o interior. O metropolitano (S500), com teor de 500ppm de enxofre, é consumido em regiões que necessitam de um óleo com menor emissão de material particulado e que produza ganho ambiental. O diesel interior (S2000), com teor de 2000ppm, é consumido nas demais regiões do país. Dentro desses dois tipos existem ainda os seguintes subtipos: óleo diesel aditivado e óleo Diesel Inverno. O óleo Diesel Marítimo se diferencia dos demais."
  },
  {
    etapa: 9,
    cena: { titulo: "Querosene", entrada: ["Querosene (destilação)"], rotulos: ["QAV-1"] },
    pergunta: "O querosene de aviação é resultado do processo de:",
    alternativas: ["Craqueamento", "Fracionamento", "Destilação"],
    correta: 2,
    explicacao:
      "O querosene para aviação (QAV) é obtido a partir do querosene resultante da destilação e suas propriedades são melhoradas na HDS (HidroDesSulfurização). A destilação também pode adequar o QAV. A hidrodessulfurização é um processo utilizado para retirar compostos de enxofre, usando hidrogênio. Esse processo melhora a qualidade desejada para o produto final, adequando-o à legislação.\n\nO querosene possui diversas características específicas, como uma ampla curva de destilação, conferindo a ele um excelente poder de solvência e uma taxa de evaporação lenta, além de um ponto de fulgor que oferece relativa segurança ao manuseio. É um produto intermediário entre a gasolina e o óleo diesel, obtido por destilação fracionada do óleo cru. Sua aplicação vai desde líquido para limpeza até como combustível para aviação."
  },
  {
    etapa: 10,
    cena: { titulo: "Unidade de Solvente", entrada: ["Nafta leve (destilação)"], rotulos: ["Nafta peróxida", "Solvente de borracha"] },
    pergunta: "Quais são os produtos gerados pela Nafta Leve após passar pela Unidade de Solvente?",
    alternativas: ["Nafta Peróxidos", "Resíduo Atmosférico", "Solvente de borracha"],
    correta: 0,
    explicacao:
      "A Nafta Leve obtida na destilação pode passar pela Unidade de Solvente para dar origem à Nafta Peróxidos, Nafta Univen e ao Solvente de Borracha.\n\nOS SOLVENTES\nOs solventes correspondem às frações especiais de hidrocarbonetos líquidos obtidos pela destilação de naftas leves e médias, que são selecionadas e refinadas. Esse produto é utilizado em processos industriais e formulações comerciais para dissolver, manter em suspensão ou servir de veículo para outros ingredientes dessas operações. Os modernos processos de refinação produzem uma grande variedade de solventes de alta pureza, grande estabilidade e diversas amplitudes de faixas e pontos de ebulição. Esses solventes são, em geral, de baixo custo por estarem disponíveis em grandes volumes e possuem uma composição química muito variada, que pode conter hidrocarbonetos parafínicos, aromáticos ou naftênicos.\n\nPara viabilizar a entrega do produto da refinaria para a Transpetro, e posteriormente às distribuidoras, são usados satélites, rádio comunicação e fibras óticas para tráfego de dados operacionais."
  }
];

const REGRAS = {
  pontosAcerto: 100,
  pontosErro: -50, // observado no original: 800 → 750 ao errar; nunca abaixo de 0
  pontuacaoMinima: 0
};
