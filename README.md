# tcc-1

## Trabalho de Conclusão de Curso

- Objetivo: Desenvolver uma API capaz de abstrair complexidades e prover dados governamentais para desenvolvedores do projeto do Ministério Público. Com isso, se for necessário, utilizar LangChain, pipelining e LLMs para ajudar no scraping das informações da API

- Planejar quais vão ser as tecnologias - stack
  - REST or GraphQL?
  - FastAPI - Python - mypy (tipagem estática) - poetry (gerenciador de dependências)

### TODO List:

- [ ] Criar projeto no github e issues
- [ ] Esboçar documento de arquitetura

### Esboço Arquitetura:

- Dependências do sistema

  - Python >= 3.12.4
  - pip >= 24.2
  - pipx >= 1.6.0
  - poetry >= 1.8.3
  - Docker >= 19.03
  - Node >= 16.20.2
  - npm >= 8.19.4
  - nginx (stable?)

- Especificações do servidor

  - Ubuntu 22.04

  - CPU Architecture: CapRover source code is compatible with any CPU architecture and the Docker build available on Docker Hub is built for AMD64 (X86), ARM64, and ARMV7 CPUs.

  - Minimum RAM: Note that the build process sometimes consumes too much RAM, and 512MB RAM might not be enough (see this issue). Most providers offer a minimum of 1GB RAM on $5 instance including DigitalOcean, Vultr, Scaleway, Linode, SSD Nodes and etc.

### Próxima Entrega:

- Criar protótipo e disponibilizar com 3 endpoints que API desenvolvida fornece que abstraem a complexidade de 3 endpoints de serviços do governo

### Referências e Materiais

- https://bdm.unb.br/bitstream/10483/31169/1/2021_AndreLuizRamosBittencourt_tcc.pdf
- https://caprover.com/docs/get-started.html
- https://rodrigolinsjr.medium.com/deploy-deapi-feita-com-fastapi-em-qualquer-servidor-de-forma-t%C3%A3o-f%C3%A1cil-quanto-um-deploy-no-heroku-a33b1db487ad
- https://docs.scrapy.org/en/latest/intro/tutorial.html
- https://mypy.readthedocs.io/en/stable/stubs.html#stub-files
