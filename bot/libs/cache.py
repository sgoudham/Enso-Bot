# Ensō~Chan - A Multi Purpose Discord Bot That Has Everything Your Server Needs!
# Copyright (C) 2020  Goudham Suresh

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# Built by karan#7508
# Edited by Hamothy#5619

import threading


class CachingCircularQueue:
    # When this lock is enabled, only the function it was called in can change
    # The state of this class
    threadLock = threading.Lock()

    def __init__(self, size):
        # The current queue
        self.values = []
        # The maximum size of the queue
        self.MAX_SIZE = size

    def increase_size(self, size):
        """Increase the size of the queue"""

    def push(self, value):
        # thread safe
        with self.threadLock:
            # If the current size is less than the max size:
            if len(self.values) < self.MAX_SIZE:
                # Add the value to the end of the queue
                self.values.append(value)
                # Return None as the default return value of Push
                return None
            else:
                # If the queue is full, add the value to the end of the list
                self.values.append(value)
                # Then remove and return the item at the start of the list
                # Therefore we don't need to touch the size
                return self.values.pop(0)

    def pop(self):
        # thread safe
        with self.threadLock:
            # should never try to pop an empty queue, you fucked up
            assert len(self.values) > 0
            # decrement the size
            # return the first value of the array
            return self.values.pop(0)

    def remove(self, value):
        # To my knowledge, this method can be called when deleting a single member and many members???
        # So this should only be called to remove a single member at a time
        with self.threadLock:
            # Remove the value inside the array (value will be a tuple that is passed in)
            # PRECONDITION, VALUE EXISTS IN CACHE, SO SHOULD EXIST IN LIST
            if value in self.values:
                self.values.remove(value)
            # As you said, to ensure concurrency, set the current size back to the length of the array


class MyCoolCache:
    threadLock = threading.Lock()

    def __init__(self, size):
        self.MAX_SIZE = size
        self.queue = CachingCircularQueue(size)
        self.cache = {}

    def decrease_size(self, size):
        """Decrease the size of the array"""

    def change_array_size(self, input_size):
        with self.threadLock:
            try:
                # Increase the size of the array and the cache to the new size
                if input_size > self.MAX_SIZE:
                    self.queue.MAX_SIZE = input_size
                    self.MAX_SIZE = input_size
                else:
                    # Split Array into 2 and iterate through the queue and delete things
                    for value in self.queue.values[input_size:]:
                        self.cache.pop(value)

                    # Make sure only the records up until the size specified are stored
                    self.queue.values = self.queue.values[:input_size]

                    # Set max size of queue and cache to be the length of the new queue
                    self.queue.MAX_SIZE = len(self.queue.values)
                    self.MAX_SIZE = len(self.queue.values)

            except Exception as e:
                print(e)

    def store_cache(self, key, dict_item):
        with self.threadLock:
            has_key = True
            # Assume the key exists in the cache
            if key in self.cache:
                # If the key is None, aka removed
                if self.cache[key] is None:
                    has_key = False
            else:
                # Or doesn't exist
                has_key = False

            # Then we don't have the key.
            # In this case, we have to check if adding a key will exceed max size
            if not has_key:
                key_to_delete = self.queue.push(key)
                # If the key is not None, that means the queue was full. We must delete an item.

                if key_to_delete is not None:
                    self.cache[key_to_delete] = None
            self.cache[key] = dict_item

    def remove_many(self, in_guild_id):
        # This method is to be used for when the bot has left a guild
        with self.threadLock:
            # Array to store keys to be removed
            keys_to_remove = []

            # For every member within the cache
            for (member_id, guild_id) in self.cache:
                # if the guild_id passed in is equal to the guild_id within the cache
                if in_guild_id == guild_id:
                    # When removing a value from the cache due to a guild leave, permanently remove all values
                    # Yes it is expensive, however as this can run concurrently and we won't need the data available
                    # For this guild, it doesn't matter how long it takes, and will save in memory in the long term
                    # Store key within array
                    keys_to_remove.append((member_id, guild_id))
                    self.queue.remove((member_id, guild_id))

            # Iterate through the array and then pop the keys from cache
            for key in keys_to_remove:
                self.cache.pop(key)
