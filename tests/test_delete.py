"""Tests for the DELETE /activities/{activity_name}/participants endpoint using AAA pattern."""
import pytest


def test_delete_participant_success(client):
    """
    Arrange: Identify existing participant
    Act: Delete the participant
    Assert: Verify deletion response is successful
    """
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={participant_email}"
    )

    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    assert participant_email in response.json()["message"]


def test_delete_participant_removes_from_list(client):
    """
    Arrange: Get initial participant count
    Act: Delete a participant
    Assert: Verify participant count decreased
    """
    # Arrange
    activity_name = "Programming Class"
    participant_email = "emma@mergington.edu"
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    client.delete(
        f"/activities/{activity_name}/participants?email={participant_email}"
    )
    updated_response = client.get("/activities")

    # Assert
    updated_count = len(updated_response.json()[activity_name]["participants"])
    assert updated_count == initial_count - 1
    assert participant_email not in updated_response.json()[activity_name]["participants"]


def test_delete_nonexistent_participant_fails(client):
    """
    Arrange: Prepare email of non-participant
    Act: Attempt to delete non-participant
    Assert: Verify 404 response
    """
    # Arrange
    activity_name = "Gym Class"
    non_participant_email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={non_participant_email}"
    )

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_delete_from_nonexistent_activity_fails(client):
    """
    Arrange: Prepare invalid activity name
    Act: Attempt to delete participant from non-existent activity
    Assert: Verify 404 response
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    participant_email = "test@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={participant_email}"
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_delete_same_participant_twice_fails(client):
    """
    Arrange: Delete a participant once (successful)
    Act: Attempt to delete the same participant again
    Assert: Verify second delete fails with 404
    """
    # Arrange
    activity_name = "Chess Club"
    participant_email = "daniel@mergington.edu"

    # First deletion should succeed
    first_response = client.delete(
        f"/activities/{activity_name}/participants?email={participant_email}"
    )
    assert first_response.status_code == 200

    # Act
    second_response = client.delete(
        f"/activities/{activity_name}/participants?email={participant_email}"
    )

    # Assert
    assert second_response.status_code == 404
