"""Tests for error handling and edge cases using AAA pattern."""
import pytest


def test_signup_without_email_parameter_fails(client):
    """
    Arrange: Prepare signup request without email query parameter
    Act: Submit request without email
    Assert: Verify request fails with validation error
    """
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422  # Unprocessable Entity


def test_delete_without_email_parameter_fails(client):
    """
    Arrange: Prepare delete request without email query parameter
    Act: Submit request without email
    Assert: Verify request fails with validation error
    """
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants")

    # Assert
    assert response.status_code == 422  # Unprocessable Entity


def test_signup_with_empty_email_string(client):
    """
    Arrange: Prepare signup with empty email string
    Act: Sign up with empty email
    Assert: Verify request is processed (API accepts empty string)
    """
    # Arrange
    activity_name = "Programming Class"
    student_email = ""

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={student_email}"
    )

    # Assert
    # API should accept the request and add empty email
    assert response.status_code == 200


def test_activity_name_case_sensitivity(client):
    """
    Arrange: Try signing up with different case variation of activity name
    Act: Sign up using exact activity name case
    Assert: Verify signup succeeds with exact case
    """
    # Arrange
    correct_activity_name = "Chess Club"
    wrong_case_activity = "chess club"
    student_email = "test@mergington.edu"

    # Act - Wrong case should fail
    response_wrong = client.post(
        f"/activities/{wrong_case_activity}/signup?email={student_email}"
    )

    # Act - Correct case should succeed
    response_correct = client.post(
        f"/activities/{correct_activity_name}/signup?email={student_email}"
    )

    # Assert
    assert response_wrong.status_code == 404
    assert response_correct.status_code == 200


def test_root_endpoint_redirects(client):
    """
    Arrange: Prepare request to root endpoint
    Act: Make request to /
    Assert: Verify redirect to static HTML
    """
    # Arrange & Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_multiple_sequential_signups(client):
    """
    Arrange: Prepare multiple unique student emails
    Act: Sign up multiple students for same activity
    Assert: Verify all signups succeed and participant list grows
    """
    # Arrange
    activity_name = "Gym Class"
    students = ["alice@test.edu", "bob@test.edu", "charlie@test.edu"]
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    for student_email in students:
        response = client.post(
            f"/activities/{activity_name}/signup?email={student_email}"
        )
        assert response.status_code == 200

    # Assert
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity_name]["participants"])
    assert final_count == initial_count + len(students)
    for student_email in students:
        assert student_email in final_response.json()[activity_name]["participants"]
