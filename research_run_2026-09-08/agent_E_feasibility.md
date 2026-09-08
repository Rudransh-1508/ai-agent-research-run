# Agent E — Experimental Feasibility Audit

**Audit date:** 2026-09-08 (Asia/Calcutta)  
**Scope:** decentralized planning/Dec-POMDPs; ad hoc teamwork and heterogeneous populations; strategic, deceptive, and costly communication; long-horizon conventions, reputation, and institutions; agentic LLM teams; mixed human-agent interaction and oversight.  
**Role boundary:** this report asks whether a scientifically sharp gap can be executed and falsified. It does not claim that any gap is novel merely because an environment exists.

## Bottom line

The strongest one-team, reasonable-compute experimental opportunities are:

1. **Reputation and cooperation under identity churn / whitewashing** in SocialJax, with an explicit warning that a 2026 non-archival Sybil study already covers simple reputation-algorithm comparisons.
2. **Active capability inference in ad hoc heterogeneous teams**, where capabilities are private, noisy, or strategically misreported, using JaxAHT/OvercookedV2 plus CAP-COMM's heterogeneous material-transport task.
3. **Verifiable strategic communication under mixed incentives**, using a small exact signaling game plus a sequential SocialJax or Melting Pot task. The experiment must separate information value, communication cost, deception, and verification.
4. **Convention repair under teammate replacement**, using OvercookedV2 and Hanabi/OpenSpiel with controlled protocol incompatibility and population turnover.
5. **Adaptive team formation under enforced information/tool partitions**, using TeamBench rather than prompt-only roles, with a single-agent unrestricted control and compute-matched controls.

All five can yield an AAMAS-scale empirical paper without training a frontier foundation model. The first four can be done with one modern GPU and CPU simulation; the fifth can use an 8B–14B open model served locally, but full benchmark sweeps remain inference-heavy.

Two superficially attractive setups are poor first choices:

- **Reproducing Alem's 1-billion-step MARL reference training** is not reasonable for a small project. Use released checkpoints and train only reduced-step baselines or a new lightweight method.
- **Using LLM personas as human substitutes** cannot support claims about people, trust, workload, or oversight. Concordia is useful for software prototyping and hypothesis generation, not human validation.

## Evidence and estimation policy

- `Observed`: stated in an official paper, project page, repository, model card, or released benchmark.
- `Estimated`: my feasibility estimate. These numbers must be replaced by pilot measurements before a proposal promises a schedule.
- Wall-clock estimates assume one RTX 4090/A5000/A6000/A100-class GPU, 16–32 CPU cores, and five independent seeds unless otherwise stated.
- A runnable repository is not the same as a reproduced result. No repository was installed or executed in this audit.
- Exact Dec-POMDP solvers are useful as oracles only on tiny horizons; neural MARL is not an exact substitute.

## Feasibility ranking

| Family | Scientific test | Environment readiness | Compute | New benchmark work | Feasibility | Main trap |
|---|---|---:|---:|---:|---:|---|
| F1. Planning with costly communication under model mismatch | High | Medium | Low–medium | Medium | **High** | 2026 selective-communication work is already close |
| F2. Active inference of private/noisy capabilities | High | High | Medium | Low–medium | **High** | Capability communication alone was studied by CAP-COMM |
| F3. Strategic, deceptive, verifiable communication | High | Medium | Medium | Medium | **High** | Easy to confound lying with channel corruption |
| F4. Reputation under churn, whitewashing, and Sybils | High | High | Low–medium | Medium | **High** | Broad Sybil/reputation comparison is no longer novel |
| F5. Convention repair under partner replacement | High | High | Medium | Medium | **High** | “Repair” and entropy/symmetry baselines are mandatory |
| F6. Institutions under endogenous compliance and enforcement | High | Medium | Medium–high | Medium–high | **Medium** | AI Economist can turn into a large unstable bilevel-RL project |
| F7. Necessity-aware LLM team formation under hard role separation | High | High | Medium–high | Low | **Medium–high** | TeamBench already studies role necessity and mixed providers |
| F8. Mid-task teammate/model replacement in long-horizon LLM teams | High | Medium | High | Medium | **Medium** | Alem calls every agent every step; full episodes are costly |
| F9. Selective human oversight in mixed teams | High | Medium | Medium + human study | Medium | **Medium** | Proxies do not validate human trust or workload |

---

## F1. Dec-POMDP planning with costly communication under execution-time model mismatch

### Precise executable question

Can decentralized agents decide **when to request information and when to replan** when the teammate or transition model may have changed, rather than assuming the centralized plan and teammate policy remain correct throughout execution?

This formulation is narrower than generic “communication-efficient MARL.” It makes model mismatch observable only through local histories and asks whether communication is worth its cost because it can diagnose and recover from coordination failure.

### Recommended environments

Use two tiers.

**Tier A — exact, diagnostic Dec-POMDPs**

- MADP Toolbox problems: Dec-Tiger, Fire Fighting, Meeting-on-a-Grid, Box Pushing, and a small warehouse rendezvous variant.
- 2 agents; 5–30 latent states for the smallest exact instances; horizon 3–10.
- Discrete private observations, discrete physical actions, and an explicit `request/share/no-message` communication action.
- Controlled mismatch: at a sampled time, change one teammate finite-state controller, observation accuracy, actuator success rate, or goal parameter.

**Tier B — scalable learned policies**

- POSGGym cooperative partially observable tasks (Pursuit-Evasion variants, Driving, Predator-Prey, Cooperative Reaching) or JaxMARL MPE/SMAX.
- 2–8 agents, horizon 50–500.
- Local vector observations and discrete/continuous environment actions; add a bandwidth-limited broadcast or point-to-point channel.

### Agents, observations, actions, communication, objective

- **Agents/count:** 2 exact-planning agents; 3–8 learned-policy agents for scaling.
- **Observation:** local state/observation history; local action/reward history; received messages. No hidden global state at execution.
- **Action:** environment action plus `communicate(target, payload)` or `request(target, field)`; communication consumes reward, bandwidth, or a time step.
- **Communication:** test reliable vs packet loss/delay, but do not combine every fault in the main experiment.
- **Objective:** expected team return minus communication cost, with separate safety/miscoordination penalties.

### Baselines

1. no communication;
2. communicate every step;
3. fixed-period and uncertainty-threshold communication;
4. centralized MPOMDP/POMDP oracle on tiny problems;
5. MADP JESP/GMAA-style policy where tractable;
6. 2026 “Asking for Information” execution rule;
7. communication-as-action MARL (IPPO/MAPPO + learned gate);
8. robust policy baselines (ROMANCE/BARDec-POMDP-style attacker training) if teammate deviations are adversarial.

### Metrics

- discounted/episodic team return;
- communication count, bytes/symbols, and cost;
- recovery latency after change;
- probability of detecting the change;
- false-alarm communication rate;
- coordination failure count;
- regret against a mismatch-aware centralized oracle on tiny instances;
- decision time and peak belief-set / controller-state size.

Report a Pareto curve over task return versus communication cost. A single scalar with a hand-picked cost coefficient is insufficient.

### Required ablations

- known change time vs unknown change time;
- teammate-policy shift vs environment shift;
- recurrent history vs current observation only;
- explicit mismatch belief vs generic RNN;
- communication request only vs request + replanning;
- shared model vs heterogeneous local models;
- reliable vs delayed/lost messages;
- matched total parameters and matched environment interactions.

### Compute and duration

- **Exact tier, estimated:** minutes to hours per small instance on CPU; a full grid over horizons and costs can run in 1–3 CPU-days. Exact solution time will grow catastrophically with horizon and observation branching.
- **Learned tier, estimated:** 5–50 million environment steps per seed; 1–3 GPU-hours per small JAX task and 6–24 hours per larger recurrent task after compilation. A 5-seed, 6-condition study is roughly 2–7 GPU-days.
- Pilot stop rule: if the exact oracle cannot solve horizon 8 or the learned baseline cannot reach stable nonzero return in 24 GPU-hours, reduce state/action branching before adding the proposed method.

### Public code/data

- MADP Toolbox: https://github.com/MADPToolbox/MADP
- POSGGym: https://github.com/RDLLab/posggym
- JaxMARL: https://github.com/FLAIROx/JaxMARL
- Mava: https://github.com/instadeepai/Mava
- SMACv2: https://github.com/oxwhirl/smacv2
- BenchMARL: https://github.com/facebookresearch/BenchMARL

### New benchmark work

Moderate. Add a versioned change-point wrapper, explicit communication accounting, small exact `.dpomdp` instances, and evaluation scripts. Do not create a new simulator.

### Feasibility / novelty danger

**Feasibility: high. Novelty danger: high unless model mismatch and recovery are central.** Garraffa et al. (2026) already decide whether communication's information value offsets cost during decentralized execution of a centralized policy. Robust and Bayesian Dec-POMDP work also covers uncertain/adversarial teammate types. A proposal about “when to communicate in Dec-POMDPs” is already addressed; the surviving executable distinction is **online change diagnosis and post-change policy repair under local observations and communication cost**.

---

## F2. Ad hoc teamwork with private, noisy, or strategically misreported capabilities

### Precise executable question

Can an ad hoc agent allocate roles and actively probe teammates when their capabilities are not known, are only partially observable through outcomes, or may be misreported?

This distinguishes a teammate's **policy convention** from its **physical/tool capability**. Existing AHT benchmarks mostly vary policies; CAP-COMM exposes heterogeneous capabilities but conditions policies on capability information and communicates it.

### Recommended environments

1. **CAP-COMM Heterogeneous Material Transport (HMT)** as the capability-grounded anchor: usually 4 robots with varying payload/sensing/mobility traits.
2. **OvercookedV2 / JaxAHT** for ad hoc policy and layout shift: 2–4 agents, asymmetric information, multiple ingredients, stochasticity, and public teammate populations.
3. **Level-Based Foraging or Multi-Robot Warehouse** for a simpler 3–8-agent scaling test where level/carrying/sensing traits can be private.

### Agents, observations, actions, communication, objective

- **Agents/count:** one controlled ego agent plus 1–7 unknown teammates; later, 2–3 controlled agents with unknown teammates for NAHT.
- **Observation:** local task state, teammate actions if visible, task outcomes, and optional self-reported capability vectors with controlled calibration/error.
- **Action:** normal task action plus bounded probe (ask, assign diagnostic subtask, request demonstration) and role/task allocation.
- **Communication:** fixed discrete messages first; natural language is unnecessary for the core MARL paper. Include truthful, noisy, stale, and strategic reports.
- **Objective:** task reward minus probe/communication delay and failure cost; evaluate fast adaptation to unseen joint capability-policy combinations.

### Baselines

- self-play IPPO/MAPPO;
- FCP, BRDiv/LBRDiv, CoMeDi teammate-population training;
- Other-Play and high-entropy symmetry-equivariant policies;
- POAM from N-Agent AHT;
- Open-OTAF team-state modelling;
- CAP-COMM capability-aware + capability communication;
- oracle with true capabilities;
- posterior inference without active probes;
- random/fixed role assignment.

### Metrics

- zero-shot return and success rate;
- adaptation regret during first K episodes / first T steps;
- capability posterior accuracy and calibration (Brier score / ECE);
- task-allocation efficiency and idle/collision/failure time;
- number and cost of probes/messages;
- worst-decile teammate performance and CVaR;
- generalization to unseen capability combinations, policies, agent counts, and layouts;
- oracle gap with known capabilities.

### Required ablations

- policy heterogeneity only vs capability heterogeneity only vs both;
- truthful vs noisy vs adversarial capability claims;
- active probes vs passive inference with identical history model;
- known vs unknown number of capability types;
- identity tokens removed;
- in-distribution vs compositional OOD capability combinations;
- one controlled agent vs controlled subteam;
- communication disabled vs costly vs free.

### Compute and duration

- **CAP-COMM reproduction:** released pretrained models allow evaluation first. Training is EPyMARL/PyTorch and likely slower; estimated 12–48 GPU-hours per seed depending on environment.
- **JaxAHT/OvercookedV2:** estimated 10–100 million steps per teammate-population run. One 24–48 GB GPU should support vectorized training. Population generation dominates: 5–20 policies × 3–5 seeds can consume 1–3 GPU-weeks if trained from scratch.
- Practical plan: reuse released NAHT/CAP-COMM/ZSC policies; generate only the new capability variants. Estimated end-to-end 1–2 weeks of serial GPU time, or 3–5 days on four GPUs.

### Public code/data

- CAP-COMM, pretrained models and HMT/HSN evaluation: https://github.com/GT-STAR-Lab/cap-comm
- JaxAHT: https://github.com/LARG/jax-aht
- ICRL4AHT (OvercookedV2, RL and heuristic teammate populations): https://github.com/AHT-Hub/ICRL4AHT
- N-Agent AHT code: https://github.com/carolinewang01/naht
- N-Agent AHT data/policies: https://huggingface.co/datasets/carolinewang01/naht
- OvercookedV2 experiments: https://github.com/overcookedv2/experiments
- ZSC-Eval policy zoo and human platform: https://github.com/sjtu-marl/ZSC-Eval
- Mava (LBF and RWARE wrappers): https://github.com/instadeepai/Mava

### New benchmark work

Low–moderate. A wrapper must sample latent capability vectors, expose controlled reports, and record inference/probe outcomes. Do not create new physics. Publish train/test composition splits and exact teammate checkpoint hashes.

### Feasibility / novelty danger

**Feasibility: high.** The strongest version uses **active information acquisition about capabilities that interact with unknown teammate conventions**, not simply heterogeneous agents or capability vectors. Open-OTAF already handles dynamic unknown teammate types and variable team size; NAHT already handles varying controlled/uncontrolled teammates; CAP-COMM already communicates heterogeneous capabilities.

---

## F3. Strategic, deceptive, costly, and verifiable communication

### Precise executable question

When agents have partially aligned incentives, can receivers learn **when to trust, verify, ignore, or challenge** a message while senders decide whether truthful signaling is worth its cost?

The key experiment must distinguish:

1. adversarial channel manipulation;
2. a self-interested sender intentionally choosing a misleading message;
3. honest but mistaken information;
4. message cost/bandwidth;
5. costly verification that reveals evidence with known reliability.

Conflating these mechanisms produces uninterpretable “deception robustness.”

### Recommended environments

**Diagnostic game:** implement a repeated Bayesian signaling/cheap-talk game in OpenSpiel with 2–5 agents, private types, continuous alignment parameter, optional audit action, and persistent identities. Because the game is small, compute equilibria/regret and enumerate policies.

**Sequential task:** use one of:

- JaxMARL `MPE_simple_world_comm_v3` or speaker-listener, extended to mixed rewards;
- SocialJax Coins, Clean Up, or PD Arena with a message and audit action;
- Melting Pot substrates involving deception, trust, reciprocation, or commons dilemmas;
- Diplomacy only as a final external-validity test, not the training centerpiece.

### Agents, observations, actions, communication, objective

- **Agents/count:** 2–5 in diagnostic games; 3–8 in sequential tasks.
- **Observation:** private type/resource/location plus public local environment; a receiver sees claimed content but not underlying evidence unless it audits.
- **Action:** physical/economic action, message from a finite vocabulary, optional evidence commitment, and audit/challenge.
- **Communication:** message cost, character/symbol budget, recipient choice, and verifiability level are factorial variables.
- **Objective:** individual return and social welfare, not only shared team return. Include a sender's incentive to mislead and a receiver's cost of false trust.

### Baselines

- no communication, full truthful oracle, and cost-free broadcast;
- TarMAC / learned receiver-addressed communication;
- IMAC information bottleneck;
- Cheap Talk Discovery and Utilization;
- emergent adversarial communication (Blumenkamp & Prorok);
- “Mis-spoke or Mis-lead” / Byzantine communication baselines;
- communication attack from “Hijacking Robot Teams” for channel manipulation;
- simple Bayesian trust/update and always-audit / never-audit;
- centralized omniscient policy on diagnostic games.

### Metrics

- each agent's return and total welfare;
- truthfulness conditional on type/incentive;
- receiver belief calibration and deception-detection AUROC;
- trust precision/recall, false-trust and false-distrust costs;
- audit frequency, audit value, and message cost;
- exploitability / NashConv in exact OpenSpiel games;
- regret against truthful and strategic populations;
- transfer to unseen incentive alignment and sender policies;
- causal utility of messages: performance after message permutation, sender masking, and evidence intervention.

### Required ablations

- sender intent vs exogenous bit flips with matched message corruption rate;
- cheap talk vs costly talk vs verifiable evidence;
- one-shot vs repeated identities;
- fixed opponent vs population of senders;
- receiver memory removed;
- public vs private audit result;
- aligned vs mixed vs opposed reward;
- semantic message content vs arbitrary discrete symbols;
- train and test on disjoint sender strategy families.

### Compute and duration

- **OpenSpiel signaling game, estimated:** CPU minutes to hours for tabular CFR/replicator/Q-learning sweeps; 1–3 days for a thorough grid.
- **JAX sequential task, estimated:** 10–100 million steps/seed; 3–24 GPU-hours/seed. Five seeds × 10 conditions is 1–3 GPU-weeks serial.
- Natural-language agents multiply cost and weaken causal control. Use them only in a held-out transfer experiment of 100–500 episodes with open 8B–14B models.

### Public code/data

- OpenSpiel: https://github.com/google-deepmind/open_spiel
- JaxMARL: https://github.com/FLAIROx/JaxMARL
- SocialJax: https://github.com/cooperativex/SocialJax
- Melting Pot: https://github.com/google-deepmind/meltingpot
- Adversarial communication paper/code lineage: https://proceedings.mlr.press/v155/blumenkamp21a.html
- Hijacking Robot Teams paper: https://proceedings.mlr.press/v229/wu23a.html
- Decrypto multi-agent reasoning environment: https://github.com/facebookresearch/decrypto
- Long-horizon deception performer/supervisor simulator: https://github.com/deeplearning-wisc/LongHorizonDeception

### New benchmark work

Moderate. The exact game is small, but the study needs a clean event log containing latent type, message, evidence, receiver belief, audit, and outcome. A sequential wrapper should reuse an existing environment.

### Feasibility / novelty danger

**Feasibility: high if discrete; medium if language-based.** Strategic communication, adversarial communication, costly communication, and deception detection all have prior work. The defensible experiment is their **controlled interaction with optional verification and repeated trust**, not another generic learned communication protocol.

---

## F4. Reputation under identity churn, whitewashing, and Sybil entry

### Precise executable question

Can decentralized agents sustain cooperation when identities are cheap, agents enter and leave, bad actors can reset their reputations, and reputation evidence may be correlated or strategically generated?

The scientifically useful outcome is a phase diagram over turnover, identity cost, evidence correlation, and observability—not a leaderboard of reputation formulas.

### Recommended environments

- **SocialJax:** Coins, Clean Up, Commons Harvest, Gift, PD Arena; 4–32 agents; vectorized JAX.
- **OpenSpiel:** repeated Prisoner's Dilemma/Public Goods/Trust Game for exact or tabular analysis.
- **Melting Pot:** held-out social scenarios for transfer/generalization after the mechanism is understood in SocialJax.
- Optional LLM transfer: CoopEval's six social dilemmas, but LLM persona results should not substitute for learned-agent or human evidence.

### Agents, observations, actions, communication, objective

- **Agents/count:** 8–32 learning agents plus 0–50% strategic entrants/Sybils; sample 4, 8, 16, 32.
- **Observation:** local interaction history, public/personal reputation signal, claimed identity age, and bounded reports from neighbors. Do not expose true controller identity.
- **Action:** task/social-dilemma action, partner selection, report/endorse, sanction, and optional identity reset with explicit cost.
- **Communication:** public reputation ledger or decentralized neighborhood gossip. Correlated reports from one controller must be traceable in the simulator but hidden from agents.
- **Objective:** individual return, social welfare, cooperation sustainability, fairness, and robustness to strategic entry.

### Baselines

- IPPO/MAPPO with no reputation;
- SVO reward shaping;
- fixed Stern Judging and simple direct reciprocity;
- Bottom-Up Reputation (AAMAS 2025);
- simple average, history-weighted, PageRank/EigenTrust-style reputation;
- perfect persistent identity oracle;
- admission cost only / no reputation;
- randomized partner selection and grim-trigger/tit-for-tat in repeated games.

### Metrics

- cooperation rate and social welfare over time;
- time to collapse and recovery after an attack wave;
- honest-agent and attacker return;
- false positive/negative partner rejection;
- reputation calibration against latent behavior type;
- inequality (Gini), exclusion of newcomers, and newcomer cold-start cost;
- attack budget required for a fixed welfare reduction;
- whitewashing gain and Sybil amplification factor;
- resilience threshold as agent population and identity cost vary.

### Required ablations

- persistent identity vs resettable identity;
- population turnover without attackers vs strategic whitewashing;
- independent Sybils vs centrally controlled correlated Sybils;
- direct experience only vs gossip;
- public vs private reputations;
- identity-reset cost sweep;
- fixed norms vs learned norms;
- stationary vs adaptive attackers;
- same total number of environment interactions across population sizes.

### Compute and duration

- **OpenSpiel/tabular tier, estimated:** CPU hours.
- **SocialJax tier, estimated:** 10–200 million steps/condition. JAX vectorization makes 8–32 agents plausible on one 24–48 GB GPU; 3–24 hours/seed depending on visual encoder and horizon. A 5-seed factorial study should budget 2–4 GPU-weeks serial.
- SocialJax reports a 50× real-time training-pipeline speedup over the official Melting Pot RLlib baseline on the authors' hardware; do not translate that into a universal wall-clock promise. Pilot locally.

### Public code/data

- SocialJax: https://github.com/cooperativex/SocialJax
- Melting Pot: https://github.com/google-deepmind/meltingpot
- OpenSpiel: https://github.com/google-deepmind/open_spiel
- Bottom-Up Reputation paper: https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1745.pdf
- AI Economist (if adding regulator/admission policy): https://github.com/salesforce/ai-economist
- CoopEval LLM social-dilemma framework: https://github.com/Xiao215/CoopEval

### New benchmark work

Moderate. Add a meta-episode population manager that persists reputation while replacing policy instances, a controller-to-pseudonym map used only for ground truth, and adversary scripts for ballot stuffing, bad-mouthing, and whitewashing.

### Feasibility / novelty danger

**Feasibility: high. Novelty confidence requires care.** A 2026 preprint “Sybil Resilience in AI Agent Reputation Networks” already compares simple average, history weighting, PageRank, and EigenTrust under three attacks, albeit in a small marketplace simulation and not archival MARL. The September 2026 “Epistemic Sybil Resistance” paper studies duplicated LLM-agent reports and correlated evidence. Therefore reject a broad “which reputation system resists Sybils?” project. The defensible AAMAS question is **co-adaptation of learned behavior, partner choice, and endogenous reputation under entry/exit and cheap identity**, with welfare and exclusion trade-offs.

---

## F5. Convention repair under teammate replacement and protocol incompatibility

### Precise executable question

When independently trained populations use incompatible conventions, can a team detect a convention mismatch and repair coordination online without globally retraining or imposing a shared language?

The dynamic event—replacement of one or more partners mid-trajectory or between closely linked episodes—is central. Static cross-play alone is already well studied.

### Recommended environments

- **OvercookedV2/JaxAHT:** 2–4 agents, controllable layouts and asymmetric information, multiple independently trained convention populations.
- **Hanabi via OpenSpiel:** 2–5 agents, constrained signaling conventions, hidden hands, legal-action masks.
- **SocialJax Gift/Coins/Clean Up:** 4–16 agents for population turnover and norm persistence.
- Optional simple language/coordination game in OpenSpiel to obtain exact convention labels and measure equilibrium selection.

### Agents, observations, actions, communication, objective

- **Agents/count:** 2–5 for convention-dense games; 8–16 for population diffusion.
- **Observation:** normal local game observation plus received legal hints/messages; no policy identity.
- **Action:** game action and existing constrained communication. Add a bounded `clarify` or convention-probe action only if the environment lacks an information action.
- **Communication:** preserve Hanabi's legal hint constraints; in Overcooked use 2–8 discrete symbols or action-mediated signaling. Avoid free-form language in the primary study.
- **Objective:** recover cooperative return rapidly after a convention shock while minimizing probe/repair cost.

### Baselines

- self-play and cross-play populations;
- Other-Play;
- FCP / BRDiv / LBRDiv / CoMeDi;
- POAM and Open-OTAF;
- high-entropy symmetry-equivariant policies (2026 work);
- Implicit Repair with RL in Emergent Communication (AAMAS 2025);
- recurrent in-context adaptation without explicit mismatch objective;
- oracle told the partner convention label.

### Metrics

- pre-shock return, immediate post-shock drop, recovery half-life, and area-under-recovery curve;
- zero-shot cross-play return;
- convention identification accuracy only where labels are behaviorally validated;
- number/cost of clarification actions;
- catastrophic interference on the original convention;
- performance under one, repeated, and simultaneous replacements;
- worst-pair and population-minimum cross-play, not only mean self-play;
- mutual information between messages/actions and latent convention, interpreted cautiously.

### Required ablations

- partner replacement vs environment change with matched observation surprise;
- explicit mismatch detector removed;
- repair memory reset vs persistent;
- one-shot adaptation vs gradient updates;
- fixed vs learned clarification policy;
- homogeneous convention populations vs intentionally incompatible populations;
- 1 replacement vs 25%, 50%, 100% turnover;
- agent identity visible vs hidden;
- entropy regularization and policy greedification baselines.

### Compute and duration

- **OvercookedV2/JaxAHT, estimated:** population generation is dominant. Reuse public teammate suites where possible; training 20 new policies × 3 seeds could take 1–3 GPU-weeks serial.
- **Hanabi/OpenSpiel evaluation:** thousands of games are CPU-cheap after policies exist. Deep recurrent training may take several GPU-days per seed.
- A practical AAMAS study can use 8–12 convention populations, 5 evaluation seeds, and two main environments in 2–4 GPU-weeks serial.

### Public code/data

- ICRL4AHT: https://github.com/AHT-Hub/ICRL4AHT
- JaxAHT: https://github.com/LARG/jax-aht
- OvercookedV2 experiments: https://github.com/overcookedv2/experiments
- OpenSpiel Hanabi: https://github.com/google-deepmind/open_spiel
- archived Hanabi Learning Environment: https://github.com/google-deepmind/hanabi-learning-environment
- N-Agent AHT policies/code: https://github.com/carolinewang01/naht
- ZSC-Eval policy zoo: https://github.com/sjtu-marl/ZSC-Eval

### New benchmark work

Moderate. Build a convention-population manifest, behavioral cross-play matrix, reproducible change-point scheduler, and recovery metrics. Do not label conventions solely by random seed; cluster behavior and validate the labels with cross-play outcomes.

### Feasibility / novelty danger

**Feasibility: high.** Static zero-shot coordination, diverse teammate populations, dynamic teammate types, and emergent-language repair all have close work. The defensible novelty must be the **controlled causal study and algorithm for recovery after protocol replacement**, especially under repeated or partial population turnover.

---

## F6. Institutions under endogenous compliance, enforcement, and strategic adaptation

### Precise executable question

Can a decentralized or bounded regulator adapt sanctions/admission/resource rules when agents strategically change behavior in response, without collapsing welfare or systematically excluding uncertain newcomers?

This is not “apply MARL to mechanism design.” The interaction of endogenous learned norms, costly enforcement, strategic adaptation, and distribution shift must be isolated.

### Recommended environments

- **SocialJax Clean Up / Commons Harvest / PD Arena:** fastest causal laboratory; 8–32 agents plus one regulator or distributed sanction actions.
- **AI Economist Foundation:** secondary validation for 4–16 worker agents and a planner with taxes/redistribution; 1,000-step episodes are supported in the official quickstart.
- **OpenSpiel public-goods or repeated social dilemmas:** small theoretical/diagnostic tier.

### Agents, observations, actions, communication, objective

- **Agents/count:** 8–32 citizens/workers; one bounded institution or peer-enforcement network.
- **Observation:** local behavior, public aggregates, delayed/noisy compliance evidence. The regulator must not see latent types.
- **Action:** ordinary task/economic action; institution sets sanction/audit/admission/tax policy at a slower timescale.
- **Communication:** public policy announcements and bounded reports; enforcement evidence has a cost and error rate.
- **Objective:** social welfare and sustainability subject to enforcement budget and distributional constraints; agents retain individual objectives.

### Baselines

- no institution, fixed hand-designed policy, omniscient planner;
- IPPO/MAPPO/SVO;
- AI Economist two-level RL;
- Bottom-Up Reputation and fixed Stern Judging;
- static tax/sanction sweep;
- robust/minimax planner;
- decentralized peer sanctions.

### Metrics

- long-run welfare/productivity/resource sustainability;
- compliance and evasion rate;
- enforcement cost and false sanctions;
- distributional welfare/Gini/minimum-agent utility;
- regret after agent-population shift;
- policy volatility and oscillation;
- exploitability by strategic entrants;
- newcomer exclusion and mobility.

### Required ablations

- fixed vs adaptive agents;
- institution update timescale;
- public vs noisy delayed monitoring;
- centralized vs peer enforcement;
- equality term removed;
- fixed population vs entry/exit;
- policy commitment vs frequent policy changes;
- same welfare objective with oracle information.

### Compute and duration

- SocialJax version: estimated 2–4 GPU-weeks serial for a strong study.
- AI Economist two-level curriculum can be unstable and version-fragile (official repository still documents Python 3.7-era setup). Estimated several GPU-weeks to months if trained fully from scratch. Treat it as transfer validation, not the only environment.

### Public code/data

- SocialJax: https://github.com/cooperativex/SocialJax
- AI Economist/Foundation: https://github.com/salesforce/ai-economist
- OpenSpiel: https://github.com/google-deepmind/open_spiel
- Melting Pot: https://github.com/google-deepmind/meltingpot

### New benchmark work

Medium–high. A two-timescale wrapper and a clean policy/evidence log are needed. If the project starts by rewriting AI Economist, scope has already failed.

### Feasibility / novelty danger

**Feasibility: medium.** Institution learning, reputation, social norms, and two-level mechanism design are mature. A publishable result needs a precise failure such as oscillation, strategic evasion, or exclusion caused by endogenous co-adaptation, with a theorem or controlled causal explanation if possible.

---

## F7. Necessity-aware LLM team formation under enforced information/tool partitions

### Precise executable question

Can a system decide whether to run solo, delegate, verify, or form a heterogeneous team based on predicted marginal team value under hard information/tool constraints and a shared token/latency budget?

TeamBench makes this executable, but it also makes generic “multi-agent roles help” claims obsolete: its public results show mean team uplift can be small, verifier false acceptance can be high, and prompt-only roles collapse behaviorally.

### Recommended environments

- **TeamBench:** main environment; 90-task verified/leaderboard subset for development and the broader task set for final evaluation. Roles are isolated in containers.
- **MultiAgentBench/MARBLE:** external validation on research, coding, database, bargaining/Werewolf scenarios.
- Optional **MLE-bench** or a small SWE-bench subset only if the project needs unrestricted repository work; both are expensive and can dilute the multi-agent question.

### Agents, observations, actions, communication, objective

- **Agents/count:** 1–4 roles: router/manager, planner, executor, verifier. Test homogeneous and heterogeneous model assignments.
- **Observation:** router sees cheap task metadata and a bounded probe; role agents receive only structurally permitted files/tools.
- **Action:** choose solo/full/reduced topology, model size, communication budget, and whether to request another round.
- **Communication:** artifact passing (plan, patch, attestation) with exact token and wall-clock accounting.
- **Objective:** deterministic task score/pass subject to dollar/token/latency budget; optimize expected utility, not raw pass rate.

### Baselines

- unrestricted single agent;
- compute-matched single agent (CoT/second pass);
- fixed full team, no-plan, no-verify, restricted executor;
- random/router-by-task-category;
- SupervisorAgent/SMAS intervention;
- auction-based cost-effective communication;
- MultiAgentBench star/chain/tree/graph protocols;
- oracle topology chosen from post-hoc outcomes.

### Metrics

- pass rate and deterministic partial score;
- Teamwork Necessity Index and marginal role contribution;
- tokens, latency, GPU/API cost, and score per unit cost;
- router regret against post-hoc best topology;
- false accept/false reject of verifier;
- role-boundary violations and failed/malformed tool calls;
- performance by solo-difficulty quantile;
- calibration of predicted team benefit;
- cross-model and cross-domain generalization.

### Required ablations

- hard container separation vs prompt-only roles;
- unrestricted solo vs equal-call/equal-token solo;
- router task metadata only vs partial execution trace;
- homogeneous vs heterogeneous models;
- verifier present/absent and deterministic test feedback present/absent;
- fixed vs adaptive turn/token budget;
- task-contamination-resistant seeds;
- remove cost term to show the policy is not merely shrinking the team.

### Compute and duration

- TeamBench notes that the full team uses 2–3× the LLM calls of the unrestricted oracle and supplies a 90-task × 5-condition sweep. One model and one seed therefore needs roughly 900–1,350 role calls plus tool execution, not counting retries.
- **Estimated local open-model pilot:** Qwen3-8B on one 24 GB GPU is plausible with moderate context; 12B–14B is safer quantized on 24 GB or BF16 on 40+ GB. Run 20–30 tasks first. Expect 1–3 days for a 90-task, 5-condition local sweep depending on context length and tool time.
- **Estimated full paper:** 3 models × 3 seeds × 90 tasks × 5 conditions can exceed 4,000 task-runs and take 1–3 GPU-weeks or substantial API spend. Use sequential confidence intervals and reserve the full sweep for final candidates.
- TeamBench warns its tested open models failed largely because of malformed function calls and 8K context overflow. Treat tool-use validity and context configuration as preconditions, not scientific outcomes.

### Public code/data/models

- TeamBench: https://github.com/ybkim95/TeamBench
- TeamBench project and protocol: https://teambench.github.io/
- MultiAgentBench/MARBLE: https://github.com/ulab-uiuc/MARBLE
- AgentVerse: https://github.com/OpenBMB/AgentVerse
- SupervisorAgent/SMAS: https://github.com/LINs-lab/SupervisorAgent
- Qwen3-8B model card: https://huggingface.co/Qwen/Qwen3-8B
- Llama 3.1 8B Instruct: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct
- vLLM OpenAI-compatible serving: https://docs.vllm.ai/en/latest/serving/openai_compatible_server/

### New benchmark work

Low. Add a learned/decision-theoretic router, prediction labels computed from existing ablations, and held-out task seeds. Do not invent another agent framework.

### Feasibility / novelty danger

**Feasibility: medium–high. Novelty danger: high.** TeamBench already defines TNI, hard role separation, five role ablations, heterogeneous provider assignment, and task-dependent uplift. SupervisorAgent and auction-based communication already reduce runtime intervention/communication. A surviving paper must contribute a **principled online team-formation decision with calibrated uncertainty and held-out structural generalization**, not merely a router prompt.

---

## F8. Mid-task teammate/model replacement in long-horizon LLM teams

### Precise executable question

Can a long-horizon team preserve a shared plan and recover coordination when one agent is replaced by a different model/policy, loses memory, or changes capability mid-task?

This is a genuine interaction problem only if the replacement changes others' optimal behavior and the benchmark includes a solo control showing the task cannot be reduced to independent subtasks.

### Recommended environments

- **Alem:** primary long-horizon, procedurally generated world; 3 agents; explicit soft specialization, communication, scratchpad memory, 27 coordination goals, up to 10,000 steps.
- **CREW-Wildfire:** secondary heterogeneous, partially observable disaster-response domain; use only after installation smoke tests because the public repository is young and Unity-based.
- **MultiAgentBench/MARBLE:** shorter validation for agent replacement in research/coding/database tasks.

### Agents, observations, actions, communication, objective

- **Agents/count:** 3 in Alem; 4–16 in CREW-Wildfire; one agent swapped at 25/50/75% progress.
- **Observation:** each agent's local state, received broadcasts, private scratchpad; replacement receives controlled subsets of prior artifacts.
- **Action:** native environment actions plus communication/scratchpad.
- **Communication:** free-form messages in Alem are broadcast each step; impose comparable character/token budgets and log private versus public memory.
- **Objective:** coordination and base-task return, survival/task completion, and recovery after replacement under a shared inference budget.

### Baselines

- no replacement;
- replacement with same model and full memory;
- replacement with same model and no memory;
- different model with transcript only;
- periodic full-state summary;
- fixed role reassignment;
- Open-OTAF / recurrent teammate inference adapted to text state;
- centralized manager;
- single-agent and independent-agent controls;
- released IPPO, HyperMARL-IPPO, MAPPO, and PQN-VDN references in Alem.

### Metrics

- normalized return split into base-task and coordination reward;
- immediate drop and recovery area after replacement;
- plan consistency and coordination-event success;
- communication volume, contradictions, and unacknowledged assignments;
- survival and achievements;
- handoff latency and duplicated work;
- performance by replacement model/capability gap;
- score per generated token and wall-clock minute.

### Required ablations

- swap policy/model vs erase memory only;
- transcript, summary, structured state, or no handoff;
- one vs repeated replacements;
- fixed vs learned replacement time;
- role-compatible vs role-incompatible replacement;
- shared prompt/model vs heterogeneous team;
- communication off / scratchpad off / both;
- reduced horizon vs canonical evaluation.

### Compute and duration

- **Critical cost warning:** Alem's language interface queries every one of three agents every environment step. At the maximum 10,000 steps, one episode can require up to 30,000 model calls. The official command evaluates 20 episodes across difficulties. Full hosted-model sweeps can therefore be extremely expensive even if episodes often terminate early.
- Use the repository's 5-step smoke test, then 100–500-step diagnostic episodes, then 5 canonical episodes; run the 20-episode protocol only for final systems.
- **Estimated local inference:** one 8B model on a 24 GB GPU, batched across three agents, could still take days for long episodes. Multiple 14B–32B models or long scratchpads likely need 48–80 GB or quantization and can take weeks.
- Do not retrain the paper's 1B-step MARL baseline. Alem releases pretrained checkpoints; reuse them.

### Public code/data/models

- Alem repository and baselines: https://github.com/alem-world/alem-env
- Alem paper: https://arxiv.org/abs/2606.08340
- CREW-Wildfire: https://github.com/generalroboticslab/CREW-Wildfire
- CREW-Wildfire paper: https://openreview.net/forum?id=8mr27qFzKR
- MultiAgentBench/MARBLE: https://github.com/ulab-uiuc/MARBLE
- vLLM: https://github.com/vllm-project/vllm

### New benchmark work

Moderate. Implement deterministic change-point wrappers and handoff conditions, and pin Alem version because its own errata notes environment-changing fixes. Record episode seeds, model revisions, prompts, decoding parameters, and all calls.

### Feasibility / novelty danger

**Feasibility: medium.** The phenomenon is valuable and Alem is unusually well suited, but inference cost is the binding constraint. A reduced diagnostic suite plus one canonical final evaluation is realistic; a giant model leaderboard is not.

---

## F9. Selective human oversight in mixed human-agent teams

### Precise executable question

When should an AI teammate ask, defer, warn, or autonomously act so that scarce human attention is spent on coordination-critical uncertainty rather than routine control?

This is different from generic human preference learning. The intervention changes the joint team's information and action allocation over time.

### Recommended environments

Use a three-stage design.

1. **Simulation/proxy stage:** AH2AC2 Hanabi with 3,079 released human games and hosted human proxy evaluation; 2- and 3-player settings.
2. **Interactive task stage:** Overcooked-AI / ZSC-Eval or COLE human platform; 2 players; 5 standard layouts plus one held-out layout.
3. **Optional larger team:** CREW platform/Wildfire for 1 human + 3–7 AI agents, only after the two-player hypothesis is established.

### Agents, observations, actions, communication, objective

- **Agents/count:** one human + one AI in Overcooked; one human/proxy + 1–2 AI in Hanabi; optional one human supervisor + 3–7 AI units.
- **Observation:** standard private/local game state; AI maintains uncertainty over partner intent/skill/convention.
- **Action:** native task actions plus `ask`, `suggest`, `warn`, `defer`, or `act`; human can accept, ignore, override, or answer.
- **Communication:** bounded choices or short messages, time-stamped; avoid unrestricted chat in the first experiment.
- **Objective:** team score minus attention/interruption cost and severe coordination failures.

### Baselines

- autonomous AI with no questions;
- ask every fixed interval / fixed uncertainty threshold;
- human has full control;
- FCP, Other-Play, COLE, ZSC-Eval agents;
- AH2AC2 baselines and human proxy;
- oracle intervention timing using future trajectory labels;
- random intervention matched by count;
- calibrated single-agent uncertainty without teammate modelling.

### Metrics

- team score/success and severe error count;
- intervention precision: fraction of asks/warnings that change the action or avert an error;
- missed-intervention rate and counterfactual value of intervention;
- human response time, number of interruptions, and workload (e.g., NASA-TLX if approved);
- trust/reliance calibration, override/acceptance rate, and post-task preference;
- adaptation to skill and convention;
- fairness across novice/experienced participant strata;
- proxy–human rank correlation, reported as validation of the proxy only on tested conditions.

### Required ablations

- teammate-model uncertainty vs generic action entropy;
- ask vs warn vs defer;
- same number of random interventions;
- proxy evaluation vs actual humans;
- novice vs experienced participants;
- visible confidence vs no confidence;
- truthful calibrated confidence vs deliberately miscalibrated control (ethics-reviewed);
- performance-only reward vs explicit attention cost.

### Compute, participants, and duration

- Proxy and AI-only experiments are cheap after models exist: CPU/GPU hours to a few days.
- **Estimated human study:** 60–120 participants, within-subject or mixed design, 30–60 minutes each; 4–8 weeks including ethics/IRB, deployment, recruitment, exclusions, and analysis. Run a 10–20-person usability pilot first.
- Human compensation, recruitment availability, and ethics approval are institutional variables; do not promise a cost before local review.
- AH2AC2 deliberately limits released human data and hosts proxy agents through a controlled evaluator. Confirm service availability before making it the sole evaluation path.

### Public code/data

- AH2AC2 code: https://github.com/FLAIROx/ah2ac2
- AH2AC2 paper: https://arxiv.org/abs/2506.21490
- Overcooked-AI and human gameplay data links: https://github.com/HumanCompatibleAI/overcooked_ai
- ZSC-Eval policies and human platform: https://github.com/sjtu-marl/ZSC-Eval
- COLE human-AI platform: https://github.com/liyang619/COLE-Platform
- CREW-Wildfire/platform: https://github.com/generalroboticslab/CREW-Wildfire

### New benchmark work

Moderate. Implement intervention UI/events, attention-cost accounting, and replay/counterfactual labels. The existing web platforms reduce engineering, but deployment and consent/data handling still require work.

### Feasibility / novelty danger

**Feasibility: medium.** Human-agent coordination and adaptive partner modelling have substantial prior work; selective intervention/oversight must be linked to a calibrated teammate uncertainty model and a measurable attention budget. Proxy-only results cannot justify human claims.

---

## Cross-family experimental standards

### Minimum comparison design

Every serious candidate should include:

1. an unrestricted or centralized upper reference where meaningful;
2. a single-agent/reduced-team control to prove multi-agent necessity;
3. no-communication and full-communication controls;
4. matched compute, parameters, environment interactions, and information;
5. at least five independent training seeds for MARL and paired environment seeds for evaluation;
6. held-out teammate policies, not merely held-out random seeds of the same algorithm;
7. a predeclared primary metric and correction for many secondary tests;
8. raw trajectory/event logs, checkpoint hashes, environment versions, and exact train/test manifests.

### Recommended staged execution

**Gate 0 — installability:** pin one environment version, run its test suite, reproduce one released checkpoint's evaluation. Stop if this takes more than three working days without a documented upstream issue/workaround.

**Gate 1 — causal toy:** demonstrate the proposed phenomenon in a tabular/exact environment with an oracle and counterexample.

**Gate 2 — baseline competence:** reproduce at least two strong baselines on one main environment before implementing the new method.

**Gate 3 — pilot power/runtime:** 3 seeds, 10–20% training budget. Estimate variance, effect size, wall time, memory, and model-call count.

**Gate 4 — full experiment:** 5–10 seeds, two environment families, held-out partner/capability/incentive shifts.

**Gate 5 — external validity:** one human or language-agent transfer only if the central controlled result survives.

### Statistical reporting

- Plot individual seeds and learning curves; do not show only a mean.
- Use paired bootstrap/permutation tests over matched evaluation seeds or partner instances.
- Report confidence intervals for return, cost, recovery time, and worst-case metrics.
- For population studies, report both per-agent and per-population uncertainty; agents sharing a training run are not independent samples.
- For human studies, participants—not episodes—are the primary independent units.
- For LLM studies, separate sampling variance, task variance, model-version variance, and tool/runtime failure.

## Feasibility traps and deceptive setups

1. **Prompt roles are not enforced roles.** If every LLM can read all state and use all tools, “planner/executor/verifier” labels do not establish multi-agent necessity. TeamBench's container separation or an equivalent access-control design is required.
2. **Multiple calls are not automatically multiple agents.** Include a compute-matched single model and an unrestricted solo agent. Reject tasks that decompose into independent calls with no strategic or informational interaction.
3. **LLM judges are not ground truth.** Prefer deterministic graders, environment rewards, exact game outcomes, or human judgments with reliability analysis.
4. **Human proxies are not humans.** AH2AC2 proxies enable cheap iteration; only a human study supports conclusions about subjective trust, workload, satisfaction, or reliance.
5. **Concordia is not a validated behavioral population.** Its Game Master and personas can introduce shared-model artifacts and circular evaluation.
6. **Exact Dec-POMDP scaling claims are dangerous.** Dec-Tiger at horizon 5 is an oracle test, not evidence of real-world scalability.
7. **SMAC/SMACv2 results are version-sensitive.** Pin StarCraft II and map versions; do not compare to numbers produced under a different binary. SMAX avoids the proprietary engine but is an approximation, not identical evidence.
8. **Official Melting Pot training code is illustrative.** Its repository explicitly says the RLlib example is not a recommended strong baseline. Use SocialJax/JaxMARL or implement/tune credible baselines.
9. **JAX compilation can fake speed comparisons.** Warm up, block until ready, and exclude/declare compilation consistently.
10. **Alem cross-paradigm scores are not head-to-head.** Its README states MARL and LLM interfaces differ in observation, communication cost, memory, and learning; compare each paradigm internally unless controls equalize these factors.
11. **Alem's per-step language calls can dominate the project.** A 10,000-step, 3-agent episode permits up to 30,000 calls. Use diagnostic horizons and released checkpoints.
12. **Training teammate populations from scratch is often the hidden cost.** Reuse released policy zoos and hash checkpoints; train only missing controlled variants.
13. **Identity leakage invalidates ad hoc teamwork.** Remove checkpoint names, agent IDs correlated with type, and fixed spawn positions; test a classifier for leakage.
14. **Correlated Sybils are not independent agents.** Evaluation must record controller-level dependence; treating 20 pseudonyms as 20 independent samples inflates significance.
15. **Communication-cost coefficients can predetermine a win.** Report the whole welfare/communication Pareto frontier.
16. **Message interpretability is not message causality.** Include permutation, masking, counterfactual, and intervention tests.
17. **One opponent family is not generalization.** Hold out algorithms/heuristics and compositional capability mixtures, not only seeds.
18. **Frontier API leaderboards are irreproducible by default.** Record model snapshots, prompts, decoding, retries, timeouts, tool schemas, and raw responses; repeat a local open-model anchor.

## Source ledger and count

### Count

- **33 unique papers / technical reports screened.** Fourteen were inspected beyond the abstract through full-text method/experiment/appendix passages or their official experiment repository; the remainder were screened at abstract plus artifact level for feasibility and overlap.
- **29 unique software, dataset, benchmark, or model artifacts inspected.**
- **62 unique paper/repository artifacts total** after deduplicating repeated search results and aliases.

This is an artifact count, not a claim that 62 full papers were read cover to cover.

### Paper / technical-report ledger (33)

1. POSGGym: a library for decision-theoretic planning and learning in partially observable, multi-agent environments (AAMAS journal, 2025): https://doi.org/10.1007/s10458-025-09716-6
2. The MADP Toolbox (JMLR, 2017): https://jmlr.org/papers/v18/17-156.html
3. SMACv2: An Improved Benchmark for Cooperative MARL (NeurIPS Datasets & Benchmarks, 2023): https://openreview.net/forum?id=5OjLGiJW3u
4. JaxMARL: Multi-Agent RL Environments and Algorithms in JAX (NeurIPS Datasets & Benchmarks, 2024): https://proceedings.neurips.cc/paper_files/paper/2024/file/5aee125f052c90e326dcf6f380df94f6-Paper-Datasets_and_Benchmarks_Track.pdf
5. BenchMARL: Benchmarking Multi-Agent Reinforcement Learning (JMLR, 2024): https://www.jmlr.org/papers/v25/23-1612.html
6. Asking for Information by Evaluating the Communication and Coordination Trade-Off in Multi-Agent POMDPs (IEEE RA-L, 2026): https://doi.org/10.1109/LRA.2026.3703246
7. Scalable Solution Methods for Dec-POMDPs with Deterministic Dynamics (AAAI, 2026): https://doi.org/10.1609/aaai.v40i43.40972
8. N-Agent Ad Hoc Teamwork (NeurIPS, 2024): https://arxiv.org/abs/2404.10740
9. Collaboration with Dynamic Open Ad Hoc Team via Team State Modelling (TMLR, 2025): https://openreview.net/forum?id=BukMU42P3G
10. Benchmarking the Limits of In-Context Reinforcement Learning for Ad-Hoc Teamwork (2026): https://arxiv.org/abs/2605.24423
11. OvercookedV2: Rethinking Overcooked for Zero-Shot Coordination (ICLR, 2025): https://openreview.net/forum?id=hlvLM3GX8R
12. ZSC-Eval: An Evaluation Toolkit and Benchmark for Multi-agent Zero-shot Coordination (NeurIPS, 2024): https://papers.neurips.cc/paper_files/paper/2024/file/54a7139c548c88e288aa0fcd2bcbeceb-Paper-Datasets_and_Benchmarks_Track.pdf
13. Generalization of Heterogeneous Multi-Robot Policies via Awareness and Communication of Capabilities (CoRL, 2023): https://openreview.net/forum?id=N3VbFUpwaa
14. The Emergence of Adversarial Communication in Multi-Agent Reinforcement Learning (CoRL): https://proceedings.mlr.press/v155/blumenkamp21a.html
15. Hijacking Robot Teams Through Adversarial Communication (CoRL, 2023): https://proceedings.mlr.press/v229/wu23a.html
16. Cheap Talk Discovery and Utilization in Multi-Agent Reinforcement Learning (ICLR, 2023): https://openreview.net/forum?id=cddbeL1HWaD
17. Learning Efficient Multi-agent Communication: An Information Bottleneck Approach (ICML, 2020): https://proceedings.mlr.press/v119/wang20i.html
18. Model-based Sparse Communication in Multi-agent Reinforcement Learning (AAMAS, 2023): https://www.southampton.ac.uk/~eg/AAMAS2023/pdfs/p439.pdf
19. Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot (ICML, 2021): https://proceedings.mlr.press/v139/leibo21a.html
20. SocialJax: An Evaluation Suite for MARL in Sequential Social Dilemmas (ICLR, 2026): https://openreview.net/forum?id=Qg6kHVN91t
21. Bottom-Up Reputation Promotes Cooperation with MARL (AAMAS, 2025): https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p1745.pdf
22. Implicit Repair with Reinforcement Learning in Emergent Communication (AAMAS, 2025): https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2115.pdf
23. OpenSpiel: A Framework for Reinforcement Learning in Games: https://arxiv.org/abs/1908.09453
24. MultiAgentBench: Evaluating the Collaboration and Competition of LLM Agents (ACL, 2025): https://aclanthology.org/2025.acl-long.421/
25. TeamBench: Evaluating Agent Coordination under Enforced Role Separation (2026): https://arxiv.org/abs/2605.07073
26. Benchmarking Open-Ended Multi-Agent Coordination in Language Agents / Alem (2026): https://arxiv.org/abs/2606.08340
27. CREW-Wildfire: Benchmarking Agentic Multi-Agent Collaborations at Scale (TMLR, 2025): https://openreview.net/forum?id=8mr27qFzKR
28. Ad-Hoc Human-AI Coordination Challenge (ICML, 2025): https://arxiv.org/abs/2506.21490
29. On the Utility of Learning about Humans for Human-AI Coordination (NeurIPS, 2019): https://arxiv.org/abs/1910.05789
30. Cost-Effective Communication: An Auction-based Method for Language Agent Interaction (AAAI, 2026): https://ojs.aaai.org/index.php/AAAI/article/view/40182
31. Epistemic Sybil Resistance: Multiplying AI Agents Without Multiplying Evidence (2026): https://arxiv.org/abs/2609.01873
32. High Entropy Leads to Symmetry-Equivariant Policies in Dec-POMDPs (2026): https://arxiv.org/abs/2511.22581
33. Bayesian Robust Cooperative Multi-Agent Reinforcement Learning Against Unknown Adversaries (ICLR, 2026): https://openreview.net/forum?id=G3gm7QBeMc

### Software / dataset / benchmark / model ledger (29)

1. POSGGym: https://github.com/RDLLab/posggym
2. MADP Toolbox: https://github.com/MADPToolbox/MADP
3. SMACv2: https://github.com/oxwhirl/smacv2
4. JaxMARL: https://github.com/FLAIROx/JaxMARL
5. BenchMARL: https://github.com/facebookresearch/BenchMARL
6. Mava: https://github.com/instadeepai/Mava
7. Melting Pot: https://github.com/google-deepmind/meltingpot
8. SocialJax: https://github.com/cooperativex/SocialJax
9. OpenSpiel: https://github.com/google-deepmind/open_spiel
10. AI Economist/Foundation: https://github.com/salesforce/ai-economist
11. CAP-COMM: https://github.com/GT-STAR-Lab/cap-comm
12. JaxAHT: https://github.com/LARG/jax-aht
13. ICRL4AHT: https://github.com/AHT-Hub/ICRL4AHT
14. N-Agent AHT code: https://github.com/carolinewang01/naht
15. N-Agent AHT data: https://huggingface.co/datasets/carolinewang01/naht
16. OvercookedV2 experiments: https://github.com/overcookedv2/experiments
17. Overcooked-AI: https://github.com/HumanCompatibleAI/overcooked_ai
18. ZSC-Eval: https://github.com/sjtu-marl/ZSC-Eval
19. AH2AC2: https://github.com/FLAIROx/ah2ac2
20. Hanabi Learning Environment (archived April 2024): https://github.com/google-deepmind/hanabi-learning-environment
21. MultiAgentBench/MARBLE: https://github.com/ulab-uiuc/MARBLE
22. TeamBench: https://github.com/ybkim95/TeamBench
23. Alem: https://github.com/alem-world/alem-env
24. CREW-Wildfire: https://github.com/generalroboticslab/CREW-Wildfire
25. Concordia generative social simulation: https://github.com/google-deepmind/concordia
26. SupervisorAgent/SMAS: https://github.com/LINs-lab/SupervisorAgent
27. LongHorizonDeception: https://github.com/deeplearning-wisc/LongHorizonDeception
28. vLLM: https://github.com/vllm-project/vllm
29. Qwen3-8B model: https://huggingface.co/Qwen/Qwen3-8B

## Recommendation to the synthesis agent

Prioritize **F2 (active private-capability inference)** or **F4 (co-adaptive reputation under identity churn)** if the goal is the best balance of AAMAS centrality, clean falsification, public infrastructure, and one-team compute. Choose **F3 (verifiable strategic communication)** if the team can support a small game-theoretic formalization. Treat F7–F9 as higher-variance projects: potentially important, but novelty, inference cost, human-subject logistics, and causal validity require stricter gates.

The most execution-ready first-week pilot is:

1. install SocialJax or JaxAHT;
2. reproduce one public baseline/checkpoint;
3. add a minimal change-point or pseudonym-reset wrapper;
4. run 3 seeds at 10% budget;
5. measure whether the claimed phenomenon exists before building the method.
