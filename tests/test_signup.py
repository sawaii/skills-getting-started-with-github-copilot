"""Tests for the POST /activities/{activity_name}/signup endpoint using AAA pattern."""
import pytest


def test_signup_success(client):
    """
    Arrange: Prepare new student email and activity name
    Act: Post signup request
    Assert: Verify student was added and response is successful
    """
    # Arrange
    activity_name = "Chess Club"
    student_email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={student_email}"
    )

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    assert student_email in response.json()["message"]


def test_signup_adds_participant(client):
    """
    Arrange: Get initial participant count
    Act: Sign up new participant
    Assert: Verify participant count increased
    """
    # Arrange
    activity_name = "Programming Class"
    student_email = "alice@mergington.edu"
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    client.post(f"/activities/{activity_name}/signup?email={student_email}")
    updated_response = client.get("/activities")

    # Assert
    updated_count = len(updated_response.json()[activity_name]["participants"])
    assert updated_count == initial_count + 1


def test_signup_duplicate_participant_fails(client):
    """
    Arrange: Prepare existing participant email
    Act: Attempt to sign up same participant twice
    Assert: Verify second signup is rejected with 400 status
    """
    # Arrange
    activity_name = "Gym Class"
    # Use an existing participant
    existing_participant = "john@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={existing_participant}"
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_fails(client):
    """
    Arrange: Prepare invalid activity name
    Act: Attempt to sign up for non-existent activity
    Assert: Verify 404 response
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    student_email = "test@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={student_email}"
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_with_special_characters_in_email(client):
    """
    Arrange: Prepare email with special characters that need encoding
    Act: Sign up with URL-encoded email
    Assert: Verify signup succeeds
    """
    # Arrange
    activity_name = "Chess Club"
    student_email = "student+test@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={student_email}"
    )

    # Assert
    assert response.status_code == 200
