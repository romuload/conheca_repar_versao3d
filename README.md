# Conheça a REPAR – Como Funciona (versão 3D)

Versão 3D do jogo "Conheça a REPAR", feito originalmente em Flash (2007) para mostrar como funciona a
Refinaria Presidente Getúlio Vargas. As 10 perguntas, as explicações e a pontuação são as do jogo original;
as cenas em SVG foram trocadas por uma maquete 3D da refinaria modelada no Blender.

## No ar
https://romuload.github.io/conheca_repar_versao3d/ — o jogo abre de dia; acrescente `?noite` ao endereço para o modo noturno.

## Como jogar
Abra `index.html` (ou a página publicada no GitHub Pages). Em cada etapa a câmera voa até a unidade,
as tubulações daquela etapa acendem e o técnico faz a pergunta. Acerto: +100 · erro: −50.
Depois do jogo, "Explorar a refinaria" permite navegar livremente pela maquete.

## Estrutura
- `index.html` — o jogo (Three.js + GSAP via CDN).
- `css/jogo3d.css` — estilos.
- `js/perguntas.js` — etapas, perguntas, alternativas e explicações.
- `js/cenas.js` — desenho do técnico (reaproveitado da versão 2D).
- `modelo/repar_glb.js` — maquete 3D (glTF com compressão Draco) embutida em JavaScript, para abrir sem servidor.
- `images/` — selo REPAR 30 anos e logo Petrobras (SVG).
- `blender/gerar_maquete_repar.py` — script que gera a maquete no Blender 5.x (unidades, equipamentos, tubulações, iluminação e câmera).

Precisa de internet para carregar Three.js, GSAP e as fontes.

## Regenerar a maquete
No console Python do Blender: `exec(open(r"caminho/para/blender/gerar_maquete_repar.py", encoding="utf-8").read())`.
Ajuste a variável `PASTA` no início do script para onde o `.blend` deve ser salvo. Depois exporte em glTF binário com compressão Draco e gere `modelo/repar_glb.js` com o conteúdo em base64.
