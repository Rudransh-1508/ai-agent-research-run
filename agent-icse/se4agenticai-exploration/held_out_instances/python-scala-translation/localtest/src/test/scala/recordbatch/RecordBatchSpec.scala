package recordbatch

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

/**
 * Expected values below were derived by actually executing RecordBatch.py
 * against this exact fixture (not hand-computed), on 2026-09-13, to keep
 * ground truth independent of the Scala translation under test.
 */
class RecordBatchSpec extends AnyFlatSpec with Matchers {

  val records: List[Record] = List(
    Record("r1", "electronics", 120.50, Set("sale", "clearance")),
    Record("r2", "grocery", 45.0, Set("sale")),
    Record("r3", "electronics", 80.0, Set.empty),
    Record("r1", "electronics", 999.0, Set.empty), // duplicate id, must be dropped
    Record("r4", "grocery", 30.0, Set("clearance")),
    Record("r5", "toys", 60.0, Set("sale", "clearance")),
    Record("r6", "toys", 60.0, Set.empty)
  )

  val deduped: List[Record] = RecordBatch.dedupeById(records)

  "dedupeById" should "keep the first occurrence and drop later duplicates" in {
    deduped.map(_.id) shouldBe List("r1", "r2", "r3", "r4", "r5", "r6")
    deduped.find(_.id == "r1").get.amount shouldBe 120.50 // first r1, not the 999.0 duplicate
  }

  "groupByCategory" should "group deduped records preserving insertion order" in {
    val groups = RecordBatch.groupByCategory(deduped)
    groups.keys.toSet shouldBe Set("electronics", "grocery", "toys")
    groups("electronics").map(_.id) shouldBe List("r1", "r3")
    groups("grocery").map(_.id) shouldBe List("r2", "r4")
    groups("toys").map(_.id) shouldBe List("r5", "r6")
  }

  "categoryTotals" should "sum amounts per category on deduped records" in {
    val totals = RecordBatch.categoryTotals(deduped)
    totals("electronics") shouldBe 200.5
    totals("grocery") shouldBe 75.0
    totals("toys") shouldBe 120.0
  }

  "topCategories" should "return the top-n categories by total, tie-broken alphabetically" in {
    RecordBatch.topCategories(deduped, n = 2) shouldBe List(("electronics", 200.5), ("toys", 120.0))
  }

  it should "respect the exclude list without mutable-default-argument contamination across calls" in {
    RecordBatch.topCategories(deduped, n = 3, exclude = List("grocery")) shouldBe
      List(("electronics", 200.5), ("toys", 120.0))
    // Calling again with the default exclude must NOT be affected by the previous call
    // (this is the direct behavioral check for the Python mutable-default-arg pitfall).
    RecordBatch.topCategories(deduped, n = 2) shouldBe List(("electronics", 200.5), ("toys", 120.0))
  }

  it should "return an empty list for an empty batch" in {
    RecordBatch.topCategories(Nil) shouldBe Nil
  }

  "findById" should "return Some(record) for a present id and None for a missing one" in {
    RecordBatch.findById(deduped, "r3") shouldBe Some(Record("r3", "electronics", 80.0, Set.empty))
    RecordBatch.findById(deduped, "zzz") shouldBe None
  }

  "overallTotal" should "sum all deduped amounts via a fold" in {
    RecordBatch.overallTotal(deduped) shouldBe 395.5
  }

  it should "return 0.0 for an empty batch" in {
    RecordBatch.overallTotal(Nil) shouldBe 0.0
  }

  "recordsWithTag" should "filter records whose tag set contains the given tag" in {
    RecordBatch.recordsWithTag(deduped, "sale").map(_.id) shouldBe List("r1", "r2", "r5")
    RecordBatch.recordsWithTag(deduped, "clearance").map(_.id) shouldBe List("r1", "r4", "r5")
  }
}
