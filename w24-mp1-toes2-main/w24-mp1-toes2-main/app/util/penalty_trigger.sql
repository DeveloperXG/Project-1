CREATE TRIGGER IF NOT EXISTS penalty_trigger
AFTER UPDATE OF end_date ON borrowings
WHEN NEW.end_date IS NOT NULL AND
((julianday(NEW.end_date) - julianday(OLD.start_date)) > 20)
BEGIN
	INSERT INTO penalties (bid, amount, paid_amount)
	VALUES (OLD.bid, julianday(NEW.end_date) - julianday(NEW.start_date) - 20, 0);
END;