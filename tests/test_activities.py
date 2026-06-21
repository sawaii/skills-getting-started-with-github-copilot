"""Tests for the GET /activities endpoint using AAA (Arrange-Act-Assert) pattern."""
import pytest


def test_get_activities_returns_all_activities(client):
    """
    Arrange: Client is set up
    Act: Make GET request to /activities
    Assert: Verify response status and activity data is returned
    """
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    for activity_name in expected_activities:
        assert activity_name in activities


def test_get_activities_returns_activity_details(client):
    """
    Arrange: Expecting specific activity structure
    Act: Get activities from endpoint
    Assert: Verify each activity has required fields
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_data in activities.values():
        for field in required_fields:
            assert field in activity_data


def test_get_activities_participants_are_lists(client):
    """
    Arrange: Expecting participants field to be a list
    Act: Fetch activities
    Assert: Verify participants field is a list
    """
    # Arrange & Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_data in activities.values():
        assert isinstance(activity_data["participants"], list)
