# OMEGA-009

New transactional adapter authenticates before journal claim and atomically persists terminal state plus HMAC evidence. Three tests cover success, tampering, failure and invalid authentication. Legacy integration remains separate; do not mix claim namespaces. Database trust, external anchor integration, worker liveness, malformed evidence handling and Android validation remain open. New tests not yet verified. No additional expenditure.
