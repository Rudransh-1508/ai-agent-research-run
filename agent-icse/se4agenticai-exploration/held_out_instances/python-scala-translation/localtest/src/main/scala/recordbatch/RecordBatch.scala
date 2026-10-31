package recordbatch

/**
 * RecordBatch module for grouping, deduplicating, and aggregating sale records.
 *
 * Scala translation of RecordBatch.py, following Scala idioms:
 * - Immutable case class for Record (Scala case classes are frozen by default,
 *   unlike Python where @dataclass(frozen=True) must be requested explicitly)
 * - No mutable-default-argument pitfall: Scala default arguments are re-evaluated
 *   per call site and safe to use directly (unlike Python's `exclude: list[str] = []`)
 * - Option instead of returning None as a sentinel
 * - scala.collection.immutable collections throughout; no var except where a
 *   local accumulator genuinely needs one, preferring foldLeft/groupBy instead
 */

final case class Record(
  id: String,
  category: String,
  amount: Double,
  tags: Set[String] = Set.empty
)

object RecordBatch {

  /** Remove duplicate records by id, keeping the first occurrence. */
  def dedupeById(records: List[Record]): List[Record] = {
    val seen = scala.collection.mutable.LinkedHashMap.empty[String, Record]
    records.foreach { r =>
      if (!seen.contains(r.id)) seen(r.id) = r
    }
    seen.values.toList
  }

  /** Group records by category, preserving insertion order within each group. */
  def groupByCategory(records: List[Record]): Map[String, List[Record]] = {
    val ordered = scala.collection.mutable.LinkedHashMap.empty[String, List[Record]]
    records.foreach { r =>
      ordered(r.category) = ordered.getOrElse(r.category, Nil) :+ r
    }
    ordered.toMap
  }

  /** Sum amounts per category. */
  def categoryTotals(records: List[Record]): Map[String, Double] =
    records.groupBy(_.category).view.mapValues(_.map(_.amount).sum).toMap

  /**
   * Return the top-n categories by total amount, excluding any category
   * named in `exclude`. Ties are broken alphabetically by category name.
   *
   * Unlike the Python original's `exclude: list[str] = []` mutable-default
   * pitfall, Scala's `exclude: List[String] = Nil` is safe: a fresh Nil is
   * bound per call, not a single shared mutable list.
   */
  def topCategories(records: List[Record], n: Int = 3, exclude: List[String] = Nil): List[(String, Double)] = {
    val totals = categoryTotals(records)
    totals.view
      .filterKeys(cat => !exclude.contains(cat))
      .toList
      .sortBy { case (cat, total) => (-total, cat) }
      .take(n)
  }

  /** Look up a record by id, returning None if not found. */
  def findById(records: List[Record], targetId: String): Option[Record] =
    records.find(_.id == targetId)

  /** Compute the overall total amount using a fold. */
  def overallTotal(records: List[Record]): Double =
    records.foldLeft(0.0)((acc, r) => acc + r.amount)

  /** Return all records whose tag set contains `tag`. */
  def recordsWithTag(records: List[Record], tag: String): List[Record] =
    records.filter(_.tags.contains(tag))
}
