import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load local environment variables from .env file
load_dotenv()

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"

# Supported Languages and their default code snippets for user testing
SUPPORTED_LANGUAGES = {
    "Python": """def calculate_factorial(n):
    # Intentional bug: no recursion termination checks
    # Security risk: none directly, but can stack overflow
    # Performance: recursive instead of iterative
    if n == 0:
        return 1
    return n * calculate_factorial(n - 1)

# Usage
print(calculate_factorial(-5))
""",
    "JavaScript": """function getUserData(userId) {
    // Intentional bug: potential SQL injection vulnerability (SQLi)
    // Readability: poor naming / nesting
    let query = "SELECT * FROM users WHERE id = '" + userId + "'";
    
    // Performance: mock network request without async/await or error handling
    let dbResult = db.execute(query);
    return dbResult;
}
""",
    "Java": """public class MathUtils {
    // Intentional bug: division by zero is not handled
    // Readability: missing documentation
    public static int divide(int a, int b) {
        return a / b;
    }
}
""",
    "C++": """#include <iostream>

// Intentional bug: buffer overflow
// Performance: pass-by-value instead of pass-by-reference
void processString(std::string str) {
    char buffer[10];
    strcpy(buffer, str.c_str());
    std::cout << "Processed: " << buffer << std::endl;
}
""",
    "SQL": """-- Intentional bug: slow query missing indices/filtering, using SELECT *
-- Best practices: using raw JOIN without explicit aliases
SELECT *
FROM orders
JOIN customers ON orders.customer_id = customers.id
WHERE order_date > '2023-01-01'
ORDER BY order_date DESC;
"""
}

# Categories of code review
CATEGORIES = [
    "Bugs & Logical Errors",
    "Security Vulnerabilities",
    "Performance Bottlenecks",
    "Readability & Style",
    "Best Practices"
]

# Severity levels and colors for UI representation
SEVERITIES = {
    "Critical": {"color": "#ef4444", "bg": "#fef2f2", "icon": "🚨"},
    "Warning": {"color": "#f97316", "bg": "#fff7ed", "icon": "⚠️"},
    "Optimization": {"color": "#3b82f6", "bg": "#eff6ff", "icon": "⚡"},
    "Info": {"color": "#10b981", "bg": "#ecfdf5", "icon": "ℹ️"}
}
