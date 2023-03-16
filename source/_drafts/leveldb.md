# leveldb

```
leveldb-1.23/
|-- db
|   |-- autocompact_test.cc
|   |-- builder.cc
|   |-- builder.h
|   |-- c.cc
|   |-- c_test.c
|   |-- corruption_test.cc
|   |-- db_impl.cc
|   |-- db_impl.h
|   |-- db_iter.cc
|   |-- db_iter.h
|   |-- db_test.cc
|   |-- dbformat.cc
|   |-- dbformat.h
|   |-- dbformat_test.cc
|   |-- dumpfile.cc
|   |-- fault_injection_test.cc
|   |-- filename.cc
|   |-- filename.h
|   |-- filename_test.cc
|   |-- leveldbutil.cc
|   |-- log_format.h
|   |-- log_reader.cc
|   |-- log_reader.h
|   |-- log_test.cc
|   |-- log_writer.cc
|   |-- log_writer.h
|   |-- memtable.cc
|   |-- memtable.h
|   |-- recovery_test.cc
|   |-- repair.cc
|   |-- skiplist.h
|   |-- skiplist_test.cc
|   |-- snapshot.h
|   |-- table_cache.cc
|   |-- table_cache.h
|   |-- version_edit.cc
|   |-- version_edit.h
|   |-- version_edit_test.cc
|   |-- version_set.cc
|   |-- version_set.h
|   |-- version_set_test.cc
|   |-- write_batch.cc
|   |-- write_batch_internal.h
|   `-- write_batch_test.cc
|-- helpers
|   `-- memenv
|       |-- memenv.cc
|       |-- memenv.h
|       `-- memenv_test.cc
|-- include
|   `-- leveldb
|       |-- c.h
|       |-- cache.h
|       |-- comparator.h                //
|       |-- db.h
|       |-- dumpfile.h
|       |-- env.h                       //
|       |-- export.h
|       |-- filter_policy.h
|       |-- iterator.h
|       |-- options.h                   //
|       |-- slice.h                     //
|       |-- status.h                    //
|       |-- table.h
|       |-- table_builder.h
|       `-- write_batch.h
|-- port
|   |-- README.md
|   |-- port.h
|   |-- port_config.h
|   |-- port_example.h
|   |-- port_stdcxx.h
|   `-- thread_annotations.h
|-- table
|   |-- block.cc
|   |-- block.h
|   |-- block_builder.cc
|   |-- block_builder.h
|   |-- filter_block.cc
|   |-- filter_block.h
|   |-- filter_block_test.cc
|   |-- format.cc
|   |-- format.h
|   |-- iterator.cc
|   |-- iterator_wrapper.h
|   |-- merger.cc
|   |-- merger.h
|   |-- table.cc
|   |-- table_builder.cc
|   |-- table_test.cc
|   |-- two_level_iterator.cc
|   `-- two_level_iterator.h
`-- util
    |-- arena.cc                        //
    |-- arena.h                         //
    |-- bloom.cc
    |-- bloom_test.cc
    |-- cache.cc
    |-- cache_test.cc
    |-- coding.cc                       //
    |-- coding.h                        //
    |-- comparator.cc                   //
    |-- crc32c.cc
    |-- crc32c.h
    |-- crc32c_test.cc
    |-- env.cc                          //
    |-- env_posix.cc
    |-- env_posix_test.cc
    |-- env_posix_test_helper.h
    |-- env_test.cc
    |-- env_windows.cc
    |-- env_windows_test.cc
    |-- env_windows_test_helper.h
    |-- filter_policy.cc
    |-- hash.cc                         //
    |-- hash.h                          //
    |-- histogram.cc
    |-- histogram.h
    |-- logging.cc
    |-- logging.h
    |-- logging_test.cc
    |-- mutexlock.h
    |-- no_destructor.h                 //
    |-- options.cc                      //
    |-- posix_logger.h
    |-- random.h                        //
    |-- status.cc                       //
    |-- testutil.cc
    |-- testutil.h
    `-- windows_logger.h
```

```
/// 11.20

// arena
const int align = (sizeof(void*) > 8) ? sizeof(void*) : 8;
static_assert((align & (align - 1)) == 0, "Pointer size should be a power of 2");
size_t current_mod = reinterpret_cast<uintptr_t>(alloc_ptr_) & (align - 1);
size_t slop = (current_mod == 0 ? 0 : align - current_mod);

// coding
// https://www.jianshu.com/p/a52c16fca39e
// https://zhuanlan.zhihu.com/p/216143729

// slice
like C++17 std::string_view

// comparator
BytewiseComparatorImpl

// NoDestructor
std::aligned_storage, placement new

// Status
// nullptr: ok
// length of message + code + message

// Options

// Env

/// 11.21

// Random
// Hash
```

