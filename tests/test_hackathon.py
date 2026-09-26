import unittest
from referees.exact import run_checks, count_cube_paths
from referees.hackathon import prepare_review, sign_human_approval, finalize_review
from tests.test_referees import job, math_pass, evidence_pass


def check(data):
    return run_checks([dict(claim_id="main", **data)], allowed_claim_ids={"main"})[0]


class ExactTests(unittest.TestCase):
    def test_cube_witness(self):
        r = check(dict(kind="hypercube_paths", dimension=3, order=[0,1,2,3,5,6,4,7], expected_total=14))
        self.assertEqual(r.status, "MATCH")
        self.assertEqual(r.scope, "ONE_LABELLING")

    def test_duplicate_order_rejected(self):
        r = check(dict(kind="hypercube_paths", dimension=1, order=[0,0], expected_total=2))
        self.assertEqual(r.status, "INVALID")

    def test_exhaustive_q3(self):
        r = check(dict(kind="hypercube_minimum", dimension=3, expected_minimum=14))
        self.assertEqual(r.status, "MATCH")
        self.assertEqual(r.actual["labellings_examined"], 40320)

    def test_wrong_minimum_refuted(self):
        r = check(dict(kind="hypercube_minimum", dimension=2, expected_minimum=4))
        self.assertEqual(r.status, "MISMATCH")
        self.assertEqual(r.actual["minimum"], 5)

    def test_partitions(self):
        r = check(dict(kind="unrestricted_partitions_allowed_parts", allowed_parts=[1,2,3,4,5],
                       expected_counts={"0":1,"1":1,"2":2,"3":3,"4":5,"5":7}))
        self.assertEqual(r.status, "MATCH")
        self.assertEqual(r.scope, "FINITE_SAMPLE")

    def test_wrong_partition_formula(self):
        r = check(dict(kind="unrestricted_partitions_allowed_parts", allowed_parts=[1,2], expected_counts={"4":4}))
        self.assertEqual(r.status, "MISMATCH")
        self.assertEqual(r.actual["counts"]["4"], 3)

    def test_disjoint_classes(self):
        r = check(dict(kind="residue_classes", classes=[{"residue":0,"modulus":2},{"residue":1,"modulus":2}],
                       require_pairwise_disjoint=True, expected_modulus_gcds=[[2,2],[2,2]]))
        self.assertEqual(r.status,"MATCH")
        self.assertEqual(r.actual["sum_class_densities"],"1")

    def test_intersection_has_valid_witness(self):
        r = check(dict(kind="residue_classes", classes=[{"residue":1,"modulus":4},{"residue":3,"modulus":6}],
                       require_pairwise_disjoint=True))
        self.assertEqual(r.status,"MISMATCH")
        x=r.actual["intersections"][0]["witness"]
        self.assertEqual(x%4,1)
        self.assertEqual(x%6,3)

    def test_rational_spherical_configuration(self):
        r=check(dict(kind="rational_vectors", vectors=[["3/5","4/5",0],[0,0,1]],
                      require_unit_norm=True, max_absolute_pairwise_dot=0))
        self.assertEqual(r.status,"MATCH")
        self.assertEqual(r.actual["dot_products"],[["1","0"],["0","1"]])

    def test_wrong_unit_claim(self):
        r=check(dict(kind="rational_vectors", vectors=[[1,1,0]], require_unit_norm=True))
        self.assertEqual(r.status,"MISMATCH")

    def test_float_not_silently_cast_to_exact(self):
        with self.assertRaises(ValueError):
            check(dict(kind="rational_vectors", vectors=[[0.6,0.8,0]], require_unit_norm=True))

    def test_executable_text_rejected_not_executed(self):
        r=check(dict(kind="rational_vectors", vectors=[["__import__('os').system('touch hacked')"]], require_unit_norm=True))
        self.assertEqual(r.status,"INVALID")


class HumanWorkflowTests(unittest.IsolatedAsyncioTestCase):
    class Backend:
        async def generate(self, *, role, **kwargs):
            return (math_pass() if role=="A" else evidence_pass()).model_dump()

    async def packet(self):
        j=job()
        j.rules.require_machine_verification=False
        return await prepare_review(j,self.Backend())

    async def test_two_passes_wait_for_human_without_lean(self):
        p=await self.packet()
        self.assertEqual(p.review_status,"READY_FOR_HUMAN")
        self.assertEqual(p.report.final_verdict,"UNKNOWN_STATUS")
        self.assertEqual(p.proposed_claim_ids,["main"])
        self.assertEqual(p.report.accepted_progress,[])

    async def test_human_approval_accepts(self):
        p=await self.packet()
        key="test-only-secret-not-a-real-key!!"
        a=sign_human_approval(p,reviewer="Test human",claim_ids=["main"],reason="TEST ONLY",secret=key)
        r=finalize_review(p,a,secret=key,current_job=p.job)
        self.assertEqual(r.final_verdict,"ACCEPT")
        self.assertEqual(r.highest_verified_cell,0)

    async def test_forged_signature_rejected(self):
        p=await self.packet()
        key="test-only-secret-not-a-real-key!!"
        a=sign_human_approval(p,reviewer="Test",claim_ids=["main"],reason="test",secret=key)
        a.signature="fake"
        with self.assertRaises(ValueError):finalize_review(p,a,secret=key,current_job=p.job)

    async def test_changed_proof_invalidates_human_approval(self):
        p=await self.packet()
        key="test-only-secret-not-a-real-key!!"
        a=sign_human_approval(p,reviewer="Test",claim_ids=["main"],reason="test",secret=key)
        current=p.job.model_copy(deep=True)
        current.candidate.proof += " changed"
        with self.assertRaises(ValueError):finalize_review(p,a,secret=key,current_job=current)

    async def test_failed_computation_blocks_approval(self):
        j=job();j.rules.require_machine_verification=False
        p=await prepare_review(j,self.Backend(),[dict(kind="hypercube_paths",claim_id="main",dimension=1,order=[0,1],expected_total=100)])
        self.assertEqual(p.report.final_verdict,"REJECT")
        with self.assertRaises(ValueError):sign_human_approval(p,reviewer="Test",claim_ids=["main"],reason="test",secret="x"*32)

    async def test_offline_does_not_invent_reviews(self):
        p=await prepare_review(job())
        self.assertIsNone(p.math.report)
        self.assertEqual(p.report.final_verdict,"UNKNOWN_STATUS")

    async def test_policy_is_not_silently_relaxed(self):
        p=await prepare_review(job(),self.Backend())
        with self.assertRaises(ValueError):sign_human_approval(p,reviewer="Test",claim_ids=["main"],reason="test",secret="x"*32)
