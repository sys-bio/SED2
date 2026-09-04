#pragma once

#include <cstddef>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

namespace sed2 {

// An ordered collection of owned T objects, each identified by its
// getId(). Backs every SED2 "list of children" attribute (e.g.
// SEDDocument's 'tasks', 'outputs', 'styles'): getAll() returns the
// ordered list, add() appends, insert() places at an index, remove()
// removes by id (Design.md, "Classes": list children need an add-/
// remove-/insert- API in addition to the usual get-/set-/isSet-/unset-).
template <class T>
class SEDList {
public:
    std::vector<T*> getAll() const {
        std::vector<T*> result;
        result.reserve(items_.size());
        for (const auto& item : items_) result.push_back(item.get());
        return result;
    }

    T* get(const std::string& id) const {
        auto it = idToIndex_.find(id);
        if (it == idToIndex_.end()) return nullptr;
        return items_[it->second].get();
    }

    T* getAt(std::size_t index) const {
        if (index >= items_.size()) return nullptr;
        return items_[index].get();
    }

    std::size_t size() const { return items_.size(); }
    bool empty() const { return items_.empty(); }

    void add(std::unique_ptr<T> item) { insert(items_.size(), std::move(item)); }

    void insert(std::size_t index, std::unique_ptr<T> item) {
        if (index > items_.size()) index = items_.size();
        items_.insert(items_.begin() + static_cast<std::ptrdiff_t>(index), std::move(item));
        reindex();
    }

    bool remove(const std::string& id) {
        auto it = idToIndex_.find(id);
        if (it == idToIndex_.end()) return false;
        items_.erase(items_.begin() + static_cast<std::ptrdiff_t>(it->second));
        reindex();
        return true;
    }

    void clear() {
        items_.clear();
        idToIndex_.clear();
    }

private:
    void reindex() {
        idToIndex_.clear();
        for (std::size_t i = 0; i < items_.size(); ++i) {
            const std::string& id = items_[i]->getId();
            if (!id.empty()) idToIndex_[id] = i;
        }
    }

    std::vector<std::unique_ptr<T>> items_;
    std::unordered_map<std::string, std::size_t> idToIndex_;
};

}  // namespace sed2
