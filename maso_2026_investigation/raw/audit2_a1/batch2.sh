#!/bin/bash
cd /Users/vanshika/ai-agent-research-run
S=maso_2026_investigation/raw/audit2_a1/arxiv_search.sh
sed -i '' 's/^sleep 3$/sleep 45/' $S
$S 'all:"delegation" AND all:"error" AND all:"multi-agent" AND all:"LLM"' "H1-delegation-error"
$S 'all:"hierarchical" AND all:"fault" AND all:"multi-agent" AND all:"LLM"' "H1-hierarchical-fault"
$S 'all:"organizational" AND all:"fault" AND all:"multi-agent" AND all:"LLM"' "H1-org-fault"
$S 'all:"cascading failures" AND all:"LLM" AND all:"agents"' "fresh-cascading"
$S 'all:"failure propagation" AND all:"LLM" AND all:"agents"' "fresh-failure-prop"
$S 'all:"backfire" AND all:"verification" AND all:"LLM"' "H3-backfire"
$S 'all:"inverted-U" AND all:"oversight"' "H3-invertedU"
$S 'all:"debate" AND all:"budget" AND all:"multi-agent" AND all:"LLM"' "H3-debate-budget"
$S 'all:"redundancy" AND all:"multi-agent" AND all:"LLM" AND all:"cost"' "H3-redundancy-cost"
$S 'all:"robustness" AND all:"multi-agent" AND all:"LLM" AND all:"recovery"' "fresh-robust-recovery"
$S 'all:"fault injection" AND all:"multi-agent" AND all:"LLM"' "fresh-fault-injection"
$S 'all:"sentinel" AND all:"multi-agent" AND all:"LLM"' "fresh-sentinel"
$S 'all:"circuit breaker" AND all:"LLM" AND all:"agent"' "fresh-circuit-breaker"
$S 'all:"quarantine" AND all:"multi-agent" AND all:"LLM"' "fresh-quarantine"
$S 'all:"error propagation" AND all:"tool" AND all:"multi-agent"' "fresh-tool-error-prop"
echo DONE
