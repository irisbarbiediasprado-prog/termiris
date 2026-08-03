# Termiris Roadmap

## ✅ Fase 1 — Runtime (concluída)

- [x] event-parser
- [x] event-bus
- [x] handlers desacoplados
- [x] runtime
- [x] pipeline FIFO
- [x] contract tests
- [x] tp-suite

---

## 🚧 Fase 2 — IA

### 2.1 MITL
- [ ] MITL publica eventos no runtime
- [ ] remover pipeline legado
- [ ] multiplexar stdin/stdout

### 2.2 Retrieve
- [ ] retrieve-handler
- [ ] context-builder
- [ ] prompt builder

### 2.3 Contexto
- [ ] memória de sessão
- [ ] memória de projeto
- [ ] replay

### 2.4 Projeto
- [ ] monitor
- [ ] notificações
- [ ] métricas

---

## ⏳ Fase 3 — Agentes

- [ ] planner
- [ ] worker
- [ ] reviewer
- [ ] certifier

---

## Regra

Cada etapa precisa terminar com:

PASS: tp-suite
