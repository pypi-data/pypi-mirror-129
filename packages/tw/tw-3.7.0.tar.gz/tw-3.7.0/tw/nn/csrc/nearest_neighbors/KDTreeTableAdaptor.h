/***********************************************************************
 * Software License Agreement (BSD License)
 *
 * Copyright 2011-16 Jose Luis Blanco (joseluisblancoc@gmail.com).
 *   All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *************************************************************************/

#pragma once

#include "nanoflann.hpp"

// #include <vector>

// ===== This example shows how to use nanoflann with these types of containers: =======
//typedef std::vector<std::vector<double> > my_vector_of_vectors_t;
//typedef std::vector<Eigen::VectorXd> my_vector_of_vectors_t;   // This requires #include <Eigen/Dense>
// =====================================================================================


/** A simple vector-of-vectors adaptor for nanoflann, without duplicating the storage.
  *  The i'th vector represents a point in the state space.
  *
  *  \tparam DIM If set to >0, it specifies a compile-time fixed dimensionality for the points in the data set, allowing more compiler optimizations.
  *  \tparam num_t The type of the point coordinates (typically, double or float).
  *  \tparam Distance The distance metric to use: nanoflann::metric_L1, nanoflann::metric_L2, nanoflann::metric_L2_Simple, etc.
  *  \tparam IndexType The type for indices in the KD-tree index (typically, size_t of int)
  */
// template <class VectorType, typename num_t = float, int DIM = -1, class Distance = nanoflann::metric_L2, typename IndexType = size_t>
// struct KDTreeVectorAdaptor
// {
// 	typedef KDTreeVectorAdaptor<VectorType,num_t,DIM,Distance> self_t;
// 	typedef typename Distance::template traits<num_t,self_t>::distance_t metric_t;
// 	typedef nanoflann::KDTreeSingleIndexAdaptor< metric_t,self_t,DIM,IndexType>  index_t;

// 	index_t* index; //! The kd-tree index for the user to call its methods as usual with any other FLANN index.
// 	size_t dims;

// 	/// Constructor: takes a const ref to the vector of vectors object with the data points
// 	KDTreeVectorAdaptor(const size_t dims /* dimensionality */, const VectorType &mat, const int leaf_max_size = 10) : m_data(mat)
// 	{
// 		assert(mat.size() != 0);
// 		this->dims= dims;
// 		index = new index_t( static_cast<int>(dims), *this /* adaptor */, nanoflann::KDTreeSingleIndexAdaptorParams(leaf_max_size ) );
// 		index->buildIndex();
// 	}

// 	~KDTreeVectorAdaptor() {
// 		delete index;
// 	}

// 	const VectorType &m_data;

// 	/** Query for the \a num_closest closest points to a given point (entered as query_point[0:dim-1]).
// 	  *  Note that this is a short-cut method for index->findNeighbors().
// 	  *  The user can also call index->... methods as desired.
// 	  * \note nChecks_IGNORED is ignored but kept for compatibility with the original FLANN interface.
// 	  */
// 	inline void query(const num_t *query_point, const size_t num_closest, IndexType *out_indices, num_t *out_distances_sq, const int nChecks_IGNORED = 10) const
// 	{
// 		nanoflann::KNNResultSet<num_t,IndexType> resultSet(num_closest);
// 		resultSet.init(out_indices, out_distances_sq);
// 		index->findNeighbors(resultSet, query_point, nanoflann::SearchParams());
// 	}

// 	/** @name Interface expected by KDTreeSingleIndexAdaptor
// 	  * @{ */

// 	const self_t & derived() const {
// 		return *this;
// 	}
// 	self_t & derived()       {
// 		return *this;
// 	}

// 	// Must return the number of data points
// 	inline size_t kdtree_get_point_count() const {
// 		return m_data.size()/this->dims;
// 	}

// 	// Returns the dim'th component of the idx'th point in the class:
// 	inline num_t kdtree_get_pt(const size_t idx, const size_t dim) const {
// 		return m_data[idx*this->dims + dim];
// 	}

// 	// Optional bounding-box computation: return false to default to a standard bbox computation loop.
// 	//   Return true if the BBOX was already computed by the class and returned in "bb" so it can be avoided to redo it again.
// 	//   Look at bb.size() to find out the expected dimensionality (e.g. 2 or 3 for point clouds)
// 	template <class BBOX>
// 	bool kdtree_get_bbox(BBOX & /*bb*/) const {
// 		return false;
// 	}

// 	/** @} */

// }; // end of KDTreeVectorOfVectorsAdaptor




template <class TableType, typename num_t = float, int DIM = -1, class Distance = nanoflann::metric_L2, typename IndexType = size_t>
struct KDTreeTableAdaptor
{
	typedef KDTreeTableAdaptor<TableType,num_t,DIM,Distance> self_t;
	typedef typename Distance::template traits<num_t,self_t>::distance_t metric_t;
	typedef nanoflann::KDTreeSingleIndexAdaptor< metric_t,self_t,DIM,IndexType>  index_t;

	index_t* index; //! The kd-tree index for the user to call its methods as usual with any other FLANN index.
	size_t dim;
	size_t npts;
	const TableType* m_data;

	/// Constructor: takes a const ref to the vector of vectors object with the data points
	KDTreeTableAdaptor(const size_t npts, const size_t dim, const TableType* mat, const int leaf_max_size = 10) : m_data(mat), dim(dim), npts(npts)
	{
		assert(npts != 0);
		index = new index_t( static_cast<int>(dim), *this /* adaptor */, nanoflann::KDTreeSingleIndexAdaptorParams(leaf_max_size ) );
		index->buildIndex();
	}

	~KDTreeTableAdaptor() {
		delete index;
	}


	/** Query for the \a num_closest closest points to a given point (entered as query_point[0:dim-1]).
	  *  Note that this is a short-cut method for index->findNeighbors().
	  *  The user can also call index->... methods as desired.
	  * \note nChecks_IGNORED is ignored but kept for compatibility with the original FLANN interface.
	  */
	inline void query(const num_t *query_point, const size_t num_closest, IndexType *out_indices, num_t *out_distances_sq, const int nChecks_IGNORED = 10) const
	{
		nanoflann::KNNResultSet<num_t,IndexType> resultSet(num_closest);
		resultSet.init(out_indices, out_distances_sq);
		index->findNeighbors(resultSet, query_point, nanoflann::SearchParams());
	}

	/** @name Interface expected by KDTreeSingleIndexAdaptor
	  * @{ */

	const self_t & derived() const {
		return *this;
	}
	self_t & derived()       {
		return *this;
	}

	// Must return the number of data points
	inline size_t kdtree_get_point_count() const {
		return this->npts;
	}

	// Returns the dim'th component of the idx'th point in the class:
	inline num_t kdtree_get_pt(const size_t pts_id, const size_t coord_id) const {
		return m_data[pts_id*this->dim + coord_id];
	}

	// Optional bounding-box computation: return false to default to a standard bbox computation loop.
	//   Return true if the BBOX was already computed by the class and returned in "bb" so it can be avoided to redo it again.
	//   Look at bb.size() to find out the expected dimensionality (e.g. 2 or 3 for point clouds)
	template <class BBOX>
	bool kdtree_get_bbox(BBOX & /*bb*/) const {
		return false;
	}

	/** @} */

}; // end of KDTreeVectorOfVectorsAdaptor

