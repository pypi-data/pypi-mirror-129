# lumo.data

```shell
pip install lumo_data
```

# howtouse

## Loky-backend DataLoader

A new DataLoader that use loky-backend multiprocess-context and new Fetcher.

```python
# from torch.utils.data import DataLoader
from lumo_data import DataLoader

loader = DataLoader(dataset=..., batch_size=..., num_workers=...)
for batch in loader:
    ...
```

## Notifiable Dataset

Override notify method, then you can write some code to cache your next batch data at one time.

```python
from lumo_data import Dataset, DataLoader


class CachedDataset(Dataset):
    ...

    def notify(self, ids):
        self.cache = []
        # sometimes, load a batch data at one time is faster than
        # load multiple sample singly. Thats the meaning of `notify`. 
        chunk = load_chuhnk_data_method(ids)
        for sample in chunk:
            self.cache.append(sample)

    def __getitem__(self, item):
        return self.cache.pop(0)


class NocacheDataset(Dataset):
    ...

    # you can also use this one like the original Dataset
    def __getitem__(self, item):
        return self.data[item]


# The DataLoader will use a new fetcher to make sure the `notify` method will be called.
loader = DataLoader(CachedDataset(), num_workers=4)
for batch in loader:
    ...
```

## Dataset Builder

# Reference

# TODO

# See also

- [lumo](https://github.com/pytorch-lumo/lumo)